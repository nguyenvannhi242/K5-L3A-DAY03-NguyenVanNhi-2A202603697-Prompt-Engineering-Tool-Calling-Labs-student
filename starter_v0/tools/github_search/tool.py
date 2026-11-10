from __future__ import annotations

import os
from typing import Any

import requests

from tools._shared import TIMEOUT, err


VALID_SORTS = {"stars", "updated", "forks"}


def search_github_repos(query: str = "", sort: str = "stars", max_results: int = 5) -> dict[str, Any]:
    try:
        cleaned_query = (query or "").strip()
        if not cleaned_query:
            raise ValueError("query must not be empty")
        if sort not in VALID_SORTS:
            raise ValueError(f"Invalid sort '{sort}'. Must be one of {sorted(VALID_SORTS)}")
        parsed_max = 5 if max_results is None else int(max_results)
        if parsed_max <= 0:
            return {"tool": "search_github_repos", "query": cleaned_query, "sort": sort, "items": []}
        parsed_max = min(parsed_max, 20)

        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": os.getenv("ARXIV_USER_AGENT", "AI20k-Day03-Research-Agent/1.0"),
        }
        token = os.getenv("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"

        response = requests.get(
            "https://api.github.com/search/repositories",
            params={"q": cleaned_query, "sort": sort, "order": "desc", "per_page": parsed_max},
            headers=headers,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        items = [{
            "title": repo.get("full_name") or repo.get("name") or "",
            "url": repo.get("html_url") or "",
            "source": "github.com",
            "summary": repo.get("description") or "",
            "stars": repo.get("stargazers_count", 0),
            "language": repo.get("language"),
        } for repo in data.get("items", [])[:parsed_max]]
        return {
            "tool": "search_github_repos",
            "query": cleaned_query,
            "sort": sort,
            "items": items,
        }
    except Exception as exc:
        return err("search_github_repos", exc)
