from __future__ import annotations

import os
from typing import Any

from providers.base import ModelResponse
from providers.openai_provider import OpenAIProvider


class DeepSeekProvider(OpenAIProvider):
    """DeepSeek API uses an OpenAI-compatible Chat Completions surface."""

    def __init__(self) -> None:
        super().__init__(
            api_key_env="DEEPSEEK_API_KEY",
            base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
            default_model=os.getenv("DEEPSEEK_MODEL", "deepseek-flash"),
        )

    def complete(
        self,
        messages: list[dict[str, str]],
        tools: list[dict[str, Any]] | None = None,
        *,
        model: str | None = None,
        temperature: float = 0.0,
        tool_choice: Any | None = None,
    ) -> ModelResponse:
        # DeepSeek-V4.1-Flash (deepseek-flash) runs in thinking mode and rejects tool_choice="required"
        effective_choice = "auto" if tool_choice == "required" else tool_choice
        return super().complete(
            messages,
            tools,
            model=model or self.default_model,
            temperature=temperature,
            tool_choice=effective_choice,
        )
