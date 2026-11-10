from __future__ import annotations

import os

from providers.openai_provider import OpenAIProvider


class OpenRouterProvider(OpenAIProvider):
    """OpenRouter uses an OpenAI-compatible Chat Completions surface."""

    def __init__(self) -> None:
        if not os.getenv("OPENROUTER_API_KEY") and os.getenv("DEEPSEEK_API_KEY"):
            super().__init__(
                api_key_env="DEEPSEEK_API_KEY",
                base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
                default_model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
            )
        else:
            super().__init__(
                api_key_env="OPENROUTER_API_KEY",
                base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
                default_model="openai/gpt-4o-mini",
            )
