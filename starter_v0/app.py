from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st

from chat import (
    ARTIFACTS_DIR,
    ROOT,
    now_iso,
    run_model_tool_loop,
    safe_slug,
    trim_history,
    write_transcript,
)
from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version


load_lab_env(ROOT)

st.set_page_config(
    page_title="AI20k Day 03 — Research Agent (DeepSeek-V4.1-Flash)",
    page_icon="🔬",
    layout="wide",
)

SAMPLE_PROMPTS = [
    "Tin tức AI hôm nay có gì nổi bật?",
    "Tweet mới nhất của Sam Altman là gì?",
    "Tìm giúp mình 5 repo GitHub nhiều sao nhất về MCP",
    "Cộng đồng Hacker News mới nhất đang thảo luận gì về DeepSeek?",
    "Đánh giá độ tin cậy (Tier mấy theo policy) của nguồn này: https://x.com/sama/status/123456",
    "Theo company policy, tweet viral có được coi là fact đã xác nhận không?",
    "Tìm paper arXiv về retrieval augmented generation evaluation.",
    "Tóm tắt 5 tweet mới nhất giúp mình",
    "Đăng bản tin này lên Telegram giúp mình",
]


def init_session() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "history" not in st.session_state:
        st.session_state.history = []
    if "turn_index" not in st.session_state:
        st.session_state.turn_index = 0
    if "transcript_id" not in st.session_state:
        ts = datetime.now().strftime("%Y%m%dT%H%M%S%f")
        st.session_state.transcript_id = f"v3_ui_deepseek_{ts}"
    if "turns_log" not in st.session_state:
        st.session_state.turns_log = []


init_session()

with st.sidebar:
    st.title("🔬 Research Agent v3")
    st.caption("Evidence-Driven Tool Calling Lab")

    provider_name = st.selectbox(
        "Provider",
        options=["deepseek", "openrouter", "openai", "gemini", "anthropic", "ollama"],
        index=0,
    )
    model_name = st.text_input("Model", value="deepseek-flash")
    version_label = st.text_input("Version Label", value="v3")
    max_rounds = st.slider("Max Tool Rounds", min_value=1, max_value=6, value=4)

    system_prompt_path = ARTIFACTS_DIR / "system_prompt.md"
    tools_path = ARTIFACTS_DIR / "tools.yaml"
    artifact_ver = build_artifact_version(version_label, system_prompt_path, tools_path)
    st.code(artifact_ver.artifact_version, language="text")

    st.subheader("🔑 API Keys Status")
    key_checks = {
        "DEEPSEEK_API_KEY": bool(os.getenv("DEEPSEEK_API_KEY")),
        "TAVILY_API_KEY": bool(os.getenv("TAVILY_API_KEY")),
        "FIRECRAWL_API_KEY": bool(os.getenv("FIRECRAWL_API_KEY")),
        "RAPIDAPI_KEY": bool(os.getenv("RAPIDAPI_KEY")),
        "TELEGRAM_BOT_TOKEN": bool(os.getenv("TELEGRAM_BOT_TOKEN")),
    }
    for k, ok in key_checks.items():
        st.write(f"{'✅' if ok else '⚪'} `{k}`")

    st.subheader("🧰 14 Declared Tools")
    declarations = load_tool_declarations(tools_path)
    for item in declarations:
        st.markdown(f"- **`{item['name']}`**")

    if st.button("🗑️ Reset Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.history = []
        st.session_state.turn_index = 0
        st.session_state.turns_log = []
        ts = datetime.now().strftime("%Y%m%dT%H%M%S%f")
        st.session_state.transcript_id = f"{safe_slug(version_label)}_ui_{safe_slug(provider_name)}_{ts}"
        st.rerun()

st.title("🔬 AI & Technology Research Agent")
st.markdown(
    "**Model:** `deepseek-flash` (DeepSeek-V4.1-Flash) &nbsp;|&nbsp; "
    "**Base Eval:** `20/20 (100%)` &nbsp;|&nbsp; "
    "**Team Group Eval:** `10/10 (100%)` &nbsp;|&nbsp; "
    "**Extension Eval:** `10/10 (100%)`"
)

with st.expander("💡 Câu hỏi mẫu (Click để gửi nhanh)", expanded=not st.session_state.messages):
    cols = st.columns(3)
    selected_sample: str | None = None
    for idx, sample in enumerate(SAMPLE_PROMPTS):
        if cols[idx % 3].button(sample, key=f"sample_{idx}", use_container_width=True):
            selected_sample = sample

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        for event in msg.get("tool_events", []):
            with st.expander(f"🔧 Tool Call: `{event['tool']}`", expanded=False):
                st.markdown("**Arguments:**")
                st.json(event.get("args", {}))
                st.markdown("**Result:**")
                st.json(event.get("result", {}))
        st.markdown(msg["content"])

user_input = st.chat_input("Nhập yêu cầu nghiên cứu của bạn...")
active_prompt = selected_sample or user_input

if active_prompt:
    st.session_state.messages.append({"role": "user", "content": active_prompt})
    with st.chat_message("user"):
        st.markdown(active_prompt)

    with st.chat_message("assistant"):
        with st.spinner("Đang phân tích và gọi công cụ..."):
            system_prompt = system_prompt_path.read_text(encoding="utf-8")
            openai_tools = to_openai_tools(declarations)
            provider = make_provider(provider_name)

            st.session_state.turn_index += 1
            turn_started = now_iso()
            messages_payload = [
                {"role": "system", "content": system_prompt},
                *trim_history(st.session_state.history, 5),
                {"role": "user", "content": active_prompt},
            ]

            turn_record: dict[str, Any] = {
                "turn_index": st.session_state.turn_index,
                "started_at": turn_started,
                "user": active_prompt,
                "status": "started",
                "assistant_text": None,
                "rounds": [],
                "tool_events": [],
            }

            try:
                result = run_model_tool_loop(
                    provider=provider,
                    messages=messages_payload,
                    tools=openai_tools,
                    model=model_name or None,
                    max_tool_rounds=max_rounds,
                )
                turn_record.update(result)
                assistant_text = result["assistant_text"]
                tool_events = result.get("tool_events", [])

                for event in tool_events:
                    with st.expander(f"🔧 Tool Call: `{event['tool']}`", expanded=True):
                        st.markdown("**Arguments:**")
                        st.json(event.get("args", {}))
                        st.markdown("**Result:**")
                        st.json(event.get("result", {}))

                st.markdown(assistant_text)
                st.session_state.history.append({"role": "user", "content": active_prompt})
                st.session_state.history.append({"role": "assistant", "content": assistant_text})
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_text,
                    "tool_events": tool_events,
                })
            except Exception as exc:
                err_msg = f"{type(exc).__name__}: {str(exc)}"
                turn_record.update({"status": "provider_error", "error": err_msg})
                st.error(err_msg)

            turn_record["ended_at"] = now_iso()
            st.session_state.turns_log.append(turn_record)

            transcript_path = ROOT / "transcripts" / f"{st.session_state.transcript_id}.transcript.json"
            transcript_payload = {
                "transcript_id": st.session_state.transcript_id,
                **artifact_version_dict(artifact_ver),
                "provider": provider_name,
                "model": model_name or getattr(provider, "default_model", None),
                "system_prompt": str(system_prompt_path),
                "tools": str(tools_path),
                "history_window": 5,
                "max_tool_rounds": max_rounds,
                "created_at": turn_started,
                "updated_at": now_iso(),
                "turns": st.session_state.turns_log,
            }
            write_transcript(transcript_path, transcript_payload)
            st.caption(f"📄 Transcript saved: `{transcript_path.name}`")
