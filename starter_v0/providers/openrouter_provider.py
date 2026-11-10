from __future__ import annotations

import os
from typing import Any

from providers.base import ModelResponse
from providers.openai_provider import OpenAIProvider


class OpenRouterProvider(OpenAIProvider):
    """OpenRouter uses an OpenAI-compatible Chat Completions surface."""

    def __init__(self) -> None:
        self._using_deepseek_fallback = not os.getenv("OPENROUTER_API_KEY") and bool(os.getenv("DEEPSEEK_API_KEY"))
        if self._using_deepseek_fallback:
            super().__init__(
                api_key_env="DEEPSEEK_API_KEY",
                base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
                default_model=os.getenv("DEEPSEEK_MODEL", "deepseek-flash"),
            )
        else:
            super().__init__(
                api_key_env="OPENROUTER_API_KEY",
                base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
                default_model="openai/gpt-4o-mini",
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
        effective_choice = "auto" if (self._using_deepseek_fallback and tool_choice == "required") else tool_choice
        return super().complete(
            messages,
            tools,
            model=model or self.default_model,
            temperature=temperature,
            tool_choice=effective_choice,
        )
