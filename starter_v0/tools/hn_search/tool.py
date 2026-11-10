from __future__ import annotations

from typing import Any

import requests

from tools._shared import TIMEOUT, domain, err


VALID_SORT_BY = {"popularity", "date"}


def search_hackernews(query: str = "", sort_by: str = "popularity", limit: int = 5) -> dict[str, Any]:
    try:
        cleaned_query = (query or "").strip()
        if not cleaned_query:
            raise ValueError("query must not be empty")
        if sort_by not in VALID_SORT_BY:
            raise ValueError(f"Invalid sort_by '{sort_by}'. Must be one of {sorted(VALID_SORT_BY)}")
        parsed_limit = 5 if limit is None else int(limit)
        if parsed_limit <= 0:
            return {"tool": "search_hackernews", "query": cleaned_query, "sort_by": sort_by, "items": []}
        parsed_limit = min(parsed_limit, 20)

        endpoint = "search_by_date" if sort_by == "date" else "search"
        response = requests.get(
            f"https://hn.algolia.com/api/v1/{endpoint}",
            params={"query": cleaned_query, "tags": "story", "hitsPerPage": parsed_limit},
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        items: list[dict[str, Any]] = []
        for hit in data.get("hits", [])[:parsed_limit]:
            object_id = hit.get("objectID") or ""
            hn_url = f"https://news.ycombinator.com/item?id={object_id}" if object_id else ""
            story_url = hit.get("url") or hn_url
            title = hit.get("title") or ""
            points = hit.get("points") or 0
            num_comments = hit.get("num_comments") or 0
            items.append({
                "title": title,
                "url": story_url,
                "hn_url": hn_url,
                "source": domain(story_url) or "news.ycombinator.com",
                "summary": f"{title} ({points} points, {num_comments} comments)",
                "points": points,
                "num_comments": num_comments,
                "author": hit.get("author"),
            })
        return {
            "tool": "search_hackernews",
            "query": cleaned_query,
            "sort_by": sort_by,
            "items": items,
        }
    except Exception as exc:
        return err("search_hackernews", exc)
