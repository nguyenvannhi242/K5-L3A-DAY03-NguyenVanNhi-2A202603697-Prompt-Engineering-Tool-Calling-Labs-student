from __future__ import annotations

import os
from typing import Any

from providers.base import ModelResponse
from providers.openai_provider import OpenAIProvider


MODEL_ALIASES = {
    "deepseek-flash": "deepseek-chat",
}


class DeepSeekProvider(OpenAIProvider):
    """DeepSeek API uses an OpenAI-compatible Chat Completions surface."""

    def __init__(self) -> None:
        super().__init__(
            api_key_env="DEEPSEEK_API_KEY",
            base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
            default_model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
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
        resolved_model = MODEL_ALIASES.get(model or "", model) if model else self.default_model
        resolved_model = MODEL_ALIASES.get(resolved_model or "", resolved_model)
        return super().complete(
            messages,
            tools,
            model=resolved_model,
            temperature=temperature,
            tool_choice=tool_choice,
        )
