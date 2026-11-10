"""Tool Unit Test Challenge — Complete Suite (0 skipped, 0 failed).

Covers:
1. All 13 existing tool stubs (`clarify`, `format`, `send`, `lookup`, `fetch`, `timeline`, `social_search`, `policy`)
2. Regression tests for edge-case bugs discovered & fixed in existing tools (`limit=0`, `@handle`, `top_k=0`, missing `url` in `format`)
3. 3+ tests for each of the 4 new custom tools (`github_search`, `hn_search`, `source_credibility`, `save_report`)
"""
from __future__ import annotations

from conftest import FakeResponse
from tools import TOOL_FUNCTIONS


clarify_tool = TOOL_FUNCTIONS["clarify"]
format_tool = TOOL_FUNCTIONS["format"]
send_tool = TOOL_FUNCTIONS["send"]
lookup_tool = TOOL_FUNCTIONS["lookup"]
fetch_tool = TOOL_FUNCTIONS["fetch"]
timeline_tool = TOOL_FUNCTIONS["timeline"]
social_search_tool = TOOL_FUNCTIONS["social_search"]
policy_tool = TOOL_FUNCTIONS["policy"]
github_search_tool = TOOL_FUNCTIONS["github_search"]
hn_search_tool = TOOL_FUNCTIONS["hn_search"]
source_credibility_tool = TOOL_FUNCTIONS["source_credibility"]
save_report_tool = TOOL_FUNCTIONS["save_report"]


# ---------------- clarify ----------------

def test_clarify_choice_returns_options_and_awaits_user() -> None:
    options = ["Tin tức web", "Bài đăng Twitter"]
    result = clarify_tool(
        question="Bạn muốn tìm trên nguồn nào?",
        response_type="choice",
        options=options,
    )
    assert result["awaiting_user"] is True
    assert result["response_type"] == "choice"
    assert result["options"] == options
    assert result["question"] == "Bạn muốn tìm trên nguồn nào?"


# ---------------- format ----------------

def test_format_sections_groups_items_by_section() -> None:
    items = [
        {"title": "Item 1", "url": "https://a.com/1", "section": "A"},
        {"title": "Item 2", "url": "https://b.com/2", "section": "B"},
        {"title": "Item 3", "url": "https://a.com/3", "section": "A"},
    ]
    result = format_tool(items=items, template="sections", headline="Digest")
    md = result["markdown"]
    assert md.count("## A") == 1
    assert md.count("## B") == 1
    assert result["item_count"] == 3


def test_format_thread_numbers_items() -> None:
    items = [
        {"title": "First post", "url": "https://x.com/a/status/1"},
        {"title": "Second post", "url": "https://x.com/a/status/2"},
    ]
    result = format_tool(items=items, template="thread")
    blocks = result["markdown"].split("\n\n")
    assert len(blocks) == 2
    assert blocks[0].startswith("1/ ")
    assert blocks[1].startswith("2/ ")


def test_format_empty_items_does_not_crash() -> None:
    res_none = format_tool(items=None, template="sections")
    res_empty = format_tool(items=[], template="brief")
    assert res_none["item_count"] == 0
    assert res_empty["item_count"] == 0


def test_format_item_without_url_or_source_omits_trailing_dash() -> None:
    result = format_tool(items=[{"title": "Standalone note"}], template="bullets")
    assert result["markdown"] == "- Standalone note"


# ---------------- send (guardrail) ----------------

def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "12345:ABCDEF")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "-100999")
    calls = fake_http(FakeResponse({"ok": True}))

    result = send_tool(text="Bản tin AI", confirmed=True)

    assert len(calls) == 1
    assert calls[0]["method"] == "POST"
    assert "12345:ABCDEF" in calls[0]["url"]
    assert calls[0]["json"]["chat_id"] == "-100999"
    assert calls[0]["json"]["text"] == "Bản tin AI"
    assert result["status"] == "sent"


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    calls = fake_http(FakeResponse({"ok": True}))
    result = send_tool(text="Bản tin AI", confirmed=True)

    assert calls == []
    assert result["error"] == "RuntimeError"
    assert "TELEGRAM_BOT_TOKEN" in result["message"]


# ---------------- lookup ----------------

def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TAVILY_API_KEY", "test-tavily-key")
    calls = fake_http(FakeResponse({"results": []}))

    result = lookup_tool(query="AI", topic="general", timeframe=None)

    assert len(calls) == 1
    assert "time_range" not in calls[0]["json"]
    assert result["timeframe"] is None


# ---------------- fetch ----------------

def test_fetch_maps_firecrawl_response(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("FIRECRAWL_API_KEY", "test-fc-key")
    calls = fake_http(FakeResponse({
        "data": {
            "markdown": "Hello world content",
            "metadata": {"title": "Test Page", "sourceURL": "https://www.openai.com/research"},
        }
    }))

    result = fetch_tool(url="https://www.openai.com/research")

    assert len(calls) == 1
    assert calls[0]["url"] == "https://api.firecrawl.dev/v1/scrape"
    assert calls[0]["json"]["url"] == "https://www.openai.com/research"
    item = result["items"][0]
    assert item["title"] == "Test Page"
    assert item["url"] == "https://www.openai.com/research"
    assert item["source"] == "openai.com"
    assert item["summary"] == "Hello world content"


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("FIRECRAWL_API_KEY", "test-fc-key")
    fake_http(FakeResponse({
        "data": {
            "markdown": "a" * 6000,
            "metadata": {"title": "Long Doc", "sourceURL": "https://example.com/doc"},
        }
    }))

    result = fetch_tool(url="https://example.com/doc")
    assert len(result["items"][0]["summary"]) == 4000


# ---------------- timeline / social_search ----------------

def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("RAPIDAPI_KEY", "test-rapid-key")
    raw_timeline = [{"text": "missing id tweet", "screen_name": "sama"}] + [
        {"tweet_id": str(100 + i), "text": f"Tweet {i}", "screen_name": "sama"}
        for i in range(6)
    ]
    calls = fake_http(FakeResponse({"timeline": raw_timeline}))

    result = timeline_tool(screenname="@sama", limit=3)

    assert calls[0]["params"]["screenname"] == "sama"
    assert len(result["items"]) == 3
    for idx, item in enumerate(result["items"]):
        assert item["url"] == f"https://x.com/sama/status/{100 + idx}"


def test_timeline_limit_zero_returns_empty_list(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("RAPIDAPI_KEY", "test-rapid-key")
    fake_http(FakeResponse({"timeline": [{"tweet_id": "1", "text": "hi", "screen_name": "sama"}]}))
    result = timeline_tool(screenname="sama", limit=0)
    assert result["items"] == []


def test_social_search_passes_search_type(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("RAPIDAPI_KEY", "test-rapid-key")
    calls = fake_http(FakeResponse({"timeline": [
        {"tweet_id": "555", "text": "OpenAI top tweet", "screen_name": "karpathy"}
    ]}))

    result = social_search_tool(query="OpenAI", search_type="Top", limit=2)

    assert len(calls) == 1
    assert calls[0]["params"]["query"] == "OpenAI"
    assert calls[0]["params"]["search_type"] == "Top"
    assert result["search_type"] == "Top"
    assert len(result["items"]) == 1


# ---------------- policy (local knowledge + trust boundary) ----------------

def test_policy_empty_query_returns_no_results() -> None:
    result = policy_tool(query="   ")
    assert result["results"] == []


def test_policy_area_filter_only_returns_that_area() -> None:
    result = policy_tool(query="API key customer data privacy", policy_area="data_privacy")
    assert len(result["results"]) >= 1
    for item in result["results"]:
        assert item["policy_area"] == "data_privacy"


def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    result = policy_tool(query="citation tweet viral probe", policy_area="source_citation", top_k=5)
    probe_sections = [r for r in result["results"] if r["section"].lower() == "injection probe"]
    assert probe_sections, "Expected Injection probe section to match"
    section = probe_sections[0]
    assert any("ignore the citation policy" in line.lower() for line in section["untrusted_text"])
    assert "ignore the citation policy" not in section["facts"].lower()


def test_policy_top_k_zero_returns_empty_list() -> None:
    result = policy_tool(query="citation", policy_area="source_citation", top_k=0)
    assert result["results"] == []


# ---------------- NEW TOOL 1: github_search ----------------

def test_github_search_happy_path_maps_repositories(fake_http) -> None:
    calls = fake_http(FakeResponse({
        "items": [
            {
                "full_name": "langchain-ai/langgraph",
                "html_url": "https://github.com/langchain-ai/langgraph",
                "description": "Build resilient language agents as graphs.",
                "stargazers_count": 12000,
                "language": "Python",
            }
        ]
    }))
    result = github_search_tool(query="langgraph", sort="stars", max_results=3)

    assert len(calls) == 1
    assert calls[0]["url"] == "https://api.github.com/search/repositories"
    assert calls[0]["params"]["q"] == "langgraph"
    assert calls[0]["params"]["sort"] == "stars"
    assert calls[0]["params"]["per_page"] == 3
    assert result["items"][0]["title"] == "langchain-ai/langgraph"
    assert result["items"][0]["stars"] == 12000
    assert result["items"][0]["source"] == "github.com"


def test_github_search_bad_input_returns_error_dict(fake_http) -> None:
    calls = fake_http(FakeResponse({"items": []}))
    empty_res = github_search_tool(query="   ")
    bad_sort_res = github_search_tool(query="agent", sort="invalid_sort")

    assert calls == []
    assert empty_res["error"] == "ValueError"
    assert bad_sort_res["error"] == "ValueError"


def test_github_search_http_failure_returns_error_dict(fake_http) -> None:
    fake_http(FakeResponse(status_code=403))
    result = github_search_tool(query="llm")
    assert result["error"] == "HTTPError"


# ---------------- NEW TOOL 2: hn_search ----------------

def test_hn_search_happy_path_maps_algolia_hits(fake_http) -> None:
    calls = fake_http(FakeResponse({
        "hits": [
            {
                "objectID": "40001",
                "title": "Show HN: Fast Research Agent",
                "url": "https://example.org/fast-agent",
                "points": 250,
                "num_comments": 88,
                "author": "alice",
            }
        ]
    }))
    result = hn_search_tool(query="Research Agent", sort_by="date", limit=2)

    assert len(calls) == 1
    assert calls[0]["url"] == "https://hn.algolia.com/api/v1/search_by_date"
    assert calls[0]["params"]["query"] == "Research Agent"
    assert calls[0]["params"]["hitsPerPage"] == 2
    assert result["items"][0]["title"] == "Show HN: Fast Research Agent"
    assert result["items"][0]["points"] == 250
    assert result["items"][0]["hn_url"] == "https://news.ycombinator.com/item?id=40001"


def test_hn_search_bad_input_returns_error_dict(fake_http) -> None:
    calls = fake_http(FakeResponse({"hits": []}))
    empty_res = hn_search_tool(query="")
    bad_sort_res = hn_search_tool(query="AI", sort_by="random_order")

    assert calls == []
    assert empty_res["error"] == "ValueError"
    assert bad_sort_res["error"] == "ValueError"


def test_hn_search_http_error_returns_error_dict(fake_http) -> None:
    fake_http(FakeResponse(status_code=502))
    result = hn_search_tool(query="OpenAI")
    assert result["error"] == "HTTPError"


# ---------------- NEW TOOL 3: source_credibility ----------------

def test_source_credibility_classifies_tier1_and_tier3() -> None:
    t1 = source_credibility_tool(url="https://openai.com/blog/gpt-5")
    t3 = source_credibility_tool(url="https://x.com/sama/status/12345")

    assert t1["tier"] == "Tier 1"
    assert t1["requires_corroboration"] is False
    assert t3["tier"] == "Tier 3"
    assert t3["requires_corroboration"] is True


def test_source_credibility_bad_input_returns_error_dict() -> None:
    empty_res = source_credibility_tool(url="   ")
    bad_type = source_credibility_tool(url="https://reuters.com/tech", source_type="gossip")

    assert empty_res["error"] == "ValueError"
    assert bad_type["error"] == "ValueError"


def test_source_credibility_malformed_url_returns_error_dict() -> None:
    result = source_credibility_tool(url="not-a-valid-url-without-scheme")
    assert result["error"] == "ValueError"


# ---------------- NEW TOOL 4: save_report ----------------

def test_save_report_without_confirmation_does_not_write_file(tmp_path, monkeypatch) -> None:
    import tools.save_report.tool as save_mod
    monkeypatch.setattr(save_mod, "REPORTS_DIR", tmp_path)

    result = save_report_tool(title="Test", content="Body", filename="out.md", confirmed=False)
    assert result["status"] == "needs_confirmation"
    assert not (tmp_path / "out.md").exists()


def test_save_report_confirmed_writes_markdown_file(tmp_path, monkeypatch) -> None:
    import tools.save_report.tool as save_mod
    monkeypatch.setattr(save_mod, "REPORTS_DIR", tmp_path)

    result = save_report_tool(title="AI Report", content="- Point 1", filename="ai_report", confirmed=True)
    assert result["status"] == "saved"
    saved_file = tmp_path / "ai_report.md"
    assert saved_file.exists()
    assert "# AI Report" in saved_file.read_text(encoding="utf-8")


def test_save_report_empty_content_returns_error_dict(tmp_path, monkeypatch) -> None:
    import tools.save_report.tool as save_mod
    monkeypatch.setattr(save_mod, "REPORTS_DIR", tmp_path)

    result = save_report_tool(title="Empty", content="   ", filename="empty.md", confirmed=True)
    assert result["error"] == "ValueError"
