from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from tools._shared import ROOT, err


REPORTS_DIR = ROOT / "saved_reports"


def _safe_filename(name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "_", (name or "").strip()).strip("._")
    if not cleaned:
        return ""
    if not cleaned.endswith(".md"):
        cleaned += ".md"
    return cleaned


def save_research_report(
    title: str = "",
    content: str = "",
    filename: str = "research_report.md",
    confirmed: bool = False,
) -> dict[str, Any]:
    try:
        cleaned_content = (content or "").strip()
        if not cleaned_content:
            raise ValueError("content must not be empty")
        safe_name = _safe_filename(filename or title or "research_report.md")
        if not safe_name:
            raise ValueError("filename is invalid")

        if not confirmed:
            return {
                "tool": "save_research_report",
                "status": "needs_confirmation",
                "filename": safe_name,
                "message": "Only save report to disk after the user explicitly confirms.",
            }

        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        out_path = REPORTS_DIR / safe_name
        full_markdown = f"# {title.strip()}\n\n{cleaned_content}\n" if title and title.strip() else f"{cleaned_content}\n"
        out_path.write_text(full_markdown, encoding="utf-8")
        return {
            "tool": "save_research_report",
            "status": "saved",
            "filename": safe_name,
            "path": str(out_path),
            "bytes_written": len(full_markdown.encode("utf-8")),
        }
    except Exception as exc:
        return err("save_research_report", exc)
