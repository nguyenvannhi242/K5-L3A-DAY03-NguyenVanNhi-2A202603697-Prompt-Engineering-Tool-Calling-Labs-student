from __future__ import annotations

from typing import Any

from tools._shared import domain, err


VALID_SOURCE_TYPES = {"auto", "official_blog", "paper", "news", "social", "forum"}

TIER_1_DOMAINS = {
    "openai.com", "anthropic.com", "deepmind.google", "ai.meta.com", "research.google",
    "arxiv.org", "nature.com", "science.org", "ieee.org", "acm.org", "sec.gov", "github.com",
}
TIER_2_DOMAINS = {
    "reuters.com", "bloomberg.com", "theverge.com", "techcrunch.com", "wired.com",
    "arstechnica.com", "MIT Technology Review", "technologyreview.com", "ft.com", "wsj.com",
}
TIER_3_DOMAINS = {
    "x.com", "twitter.com", "reddit.com", "news.ycombinator.com", "medium.com", "facebook.com", "t.me",
}


def check_source_credibility(url: str = "", source_type: str = "auto") -> dict[str, Any]:
    try:
        cleaned_url = (url or "").strip()
        if not cleaned_url:
            raise ValueError("url must not be empty")
        if source_type not in VALID_SOURCE_TYPES:
            raise ValueError(f"Invalid source_type '{source_type}'. Must be one of {sorted(VALID_SOURCE_TYPES)}")

        host = domain(cleaned_url).lower()
        if not host and "://" not in cleaned_url:
            raise ValueError("url must be a valid HTTP/HTTPS URL")

        if source_type in {"official_blog", "paper"} or host in TIER_1_DOMAINS or host.endswith(".gov") or host.endswith(".edu"):
            tier = "Tier 1"
            requires_corroboration = False
            reason = "Primary source (official blog, academic paper, documentation, or institutional domain)."
        elif source_type == "news" or host in TIER_2_DOMAINS:
            tier = "Tier 2"
            requires_corroboration = False
            reason = "Reputable reporting / tech journalism that links to primary evidence."
        elif source_type in {"social", "forum"} or host in TIER_3_DOMAINS:
            tier = "Tier 3"
            requires_corroboration = True
            reason = "Social media or community forum post. Treat as early signal only; requires Tier 1/2 corroboration."
        else:
            tier = "Tier 3"
            requires_corroboration = True
            reason = "Unverified or unknown external domain. Treat as signal until corroborated by Tier 1/2 source."

        return {
            "tool": "check_source_credibility",
            "url": cleaned_url,
            "domain": host,
            "source_type": source_type,
            "tier": tier,
            "requires_corroboration": requires_corroboration,
            "reason": reason,
        }
    except Exception as exc:
        return err("check_source_credibility", exc)
