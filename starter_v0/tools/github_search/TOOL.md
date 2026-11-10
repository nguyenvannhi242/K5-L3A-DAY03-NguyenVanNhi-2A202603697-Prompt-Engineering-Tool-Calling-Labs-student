---
name: github_search
track: bonus
kind: live_api
provider: GitHub REST API
requires_env: []
inputs: [query, sort, max_results]
outputs: [items]
side_effect: false
---
# github_search

Searches open-source GitHub repositories by keyword or topic via the GitHub Search API.
Returns repository full name, URL, description, star count, and primary language.
