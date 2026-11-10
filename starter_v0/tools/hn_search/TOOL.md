---
name: hn_search
track: bonus
kind: live_api
provider: Hacker News Algolia API
requires_env: []
inputs: [query, sort_by, limit]
outputs: [items]
side_effect: false
---
# hn_search

Searches Hacker News stories and developer discussions via the Algolia HN Search API.
Supports sorting by `popularity` (points) or `date` (newest).
