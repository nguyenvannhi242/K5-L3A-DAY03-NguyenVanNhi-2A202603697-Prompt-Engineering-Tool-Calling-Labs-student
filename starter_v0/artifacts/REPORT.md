# Day 03 Lab v2 Report — Research Agent

> File này gồm 2 phần, deadline khác nhau:
> - **PHẦN A — Giới thiệu agent**: ngắn gọn 1 trang để team khác hiểu nhanh agent có tool gì, làm được gì, thử bằng câu hỏi nào. **Xong trước 16:30** để làm tài liệu phụ trợ khi demo. Có thể làm thành poster HTML/SVG (`artifacts/poster.html` / `poster.svg`) để show cho team cùng zone.
> - **PHẦN B — Chi tiết / Bằng chứng**: bảng đầy đủ (v0–v3, failure, eval, chat) dựa trên log thật. **Có thể hoàn thiện sau buổi debate để nộp bài.**

## Team

- Team: K5-L3A-DAY03 — Nguyễn Văn Nhì (`2A202603697`)
- Members: Nguyễn Văn Nhì
- Provider/model: `deepseek` / `deepseek-flash` (DeepSeek-V4.1-Flash)

---

# PHẦN A — Giới thiệu agent

## A1. Agent này làm được gì

**AI & Technology Research Agent** là trợ lý nghiên cứu công nghệ đa nguồn dựa trên bằng chứng (evidence-driven): tự động định tuyến và tra cứu tin tức thời sự (Tavily), thảo luận mạng xã hội Twitter/X (RapidAPI) & Hacker News (Algolia), kho mã nguồn mở GitHub, bài báo khoa học arXiv, quy định nội bộ công ty (`company_policy`), đánh giá cấp độ tin cậy của nguồn tin (`Tier 1/2/3`), tổng hợp thành bản tin Markdown chuẩn hóa và xuất file hoặc đăng lên kênh Telegram khi có sự xác nhận rõ ràng của người dùng.

**Link dùng thử (deploy):**

> Chạy local bằng lệnh `streamlit run app.py` (tại thư mục `starter_v0`) và mở tunnel bằng `cloudflared tunnel --url http://localhost:8501`.
>
> URL: `http://localhost:8501` (hoặc link `https://<random>.trycloudflare.com` khi bật Cloudflare Tunnel trong phiên demo)

## A2. Tool agent có

Agent được trang bị tổng cộng **14 công cụ** (6 Core + 4 Bonus có sẵn + **4 Tool mới do nhóm tự phát triển**):

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| `clarify` | Hỏi lại người dùng khi thiếu thông tin bắt buộc (handle, URL) hoặc hỏi xác nhận (`yes_no`) trước khi gửi/lưu | không |
| `timeline` | Lấy các bài đăng (tweet) gần đây nhất từ một tài khoản Twitter/X cụ thể (`screenname`) | không |
| `social_search` | Tìm kiếm bài đăng Twitter/X theo chủ đề/từ khóa (`Latest` hoặc `Top`) | không |
| `lookup` | Tìm kiếm thông tin hoặc tin tức thời sự (`topic=news|general`, `timeframe=day|week|month|year`) trên web qua Tavily | không |
| `fetch` | Đọc và trích xuất nội dung Markdown từ một đường dẫn URL cụ thể qua Firecrawl | không |
| `format` | Trình bày danh sách dữ liệu đã thu thập thành bản tin Markdown theo khuôn mẫu (`brief`, `sections`, `bullets`, `thread`, `daily_ai_vn`) | không |
| `send` | Đăng bản tin Markdown lên kênh Telegram (có guardrail bắt buộc xác nhận `confirmed=true`) | không |
| `policy` | Tra cứu sổ tay quy định nội bộ công ty (`ai_research`, `source_citation`, `data_privacy`, `external_publishing`, `tool_usage`) kèm tách biệt `untrusted_text` | không |
| `papers` | Tìm kiếm bài báo khoa học / preprint trên arXiv theo từ khóa | không |
| `paper_text` | Tải PDF bài báo từ arXiv và trích xuất văn bản cục bộ theo số trang giới hạn | không |
| **`github_search`** | Tìm kiếm kho mã nguồn mở (repositories) trên GitHub REST API theo từ khóa và sắp xếp theo `stars`, `updated`, hoặc `forks` | **Có (Tool mới #1)** |
| **`hn_search`** | Tìm kiếm bài viết và thảo luận kỹ thuật của lập trình viên trên Hacker News (Algolia API) theo độ phổ biến (`popularity`) hoặc mới nhất (`date`) | **Có (Tool mới #2)** |
| **`source_credibility`** | Đánh giá cấp độ tin cậy (`Tier 1`, `Tier 2`, `Tier 3`) và yêu cầu kiểm chứng chéo của một URL theo chuẩn Company Source Citation Policy | **Có (Tool mới #3)** |
| **`save_report`** | Lưu bản báo cáo/bản tin nghiên cứu ra file `.md` cục bộ trong `saved_reports/` (có guardrail bắt buộc xác nhận `confirmed=true`) | **Có (Tool mới #4)** |

## A3. Câu hỏi mẫu để thử

1. **Tra cứu tin tức & tổng hợp tự động:** `"Tin tức AI hôm nay có gì nổi bật?"`
2. **Tìm kiếm mã nguồn mở (Tool mới `github_search`):** `"Tìm giúp mình 5 repo GitHub nhiều sao nhất về MCP"`
3. **Thảo luận cộng đồng kỹ thuật (Tool mới `hn_search`):** `"Cộng đồng Hacker News mới nhất đang thảo luận gì về DeepSeek?"`
4. **Kiểm tra độ tin cậy nguồn trích dẫn (Tool mới `source_credibility`):** `"Đánh giá độ tin cậy (Tier mấy theo policy) của nguồn này: https://x.com/sama/status/123456"`
5. **Kiểm tra hỏi lại khi thiếu thông tin & guardrail xác nhận:** `"Tóm tắt 3 tweet mới nhất giúp mình"` -> trả lời `"Của Sam Altman nhé"` -> `"Đăng bản tin vừa rồi lên Telegram giúp mình"`.

---

# PHẦN B — Chi tiết / Bằng chứng

## B1. Version Evidence

Dữ liệu trích xuất trực tiếp từ [`artifacts/version_log.csv`](version_log.csv) và các file log trong [`runs/`](../runs/) trên model **`deepseek-flash`**:

| Version | Changed Artifact | Hypothesis | Metric Before (`case_accuracy`) | Metric After (`case_accuracy`) | Run File |
|---|---|---|---:|---:|---|
| `v0` | `baseline` | Đo hành vi baseline của `starter_v0` với model `deepseek-flash` trước khi tối ưu prompt và tool declarations (`routing=0.70`, `arg=0.55`, `multiturn=0.6667`). | — | `0.55` (11/20) | [`v0_B_base_deepseek_20261110T121637166053.json`](../runs/v0_B_base_deepseek_20261110T121637166053.json) |
| `v1` | `system_prompt.md` | Loại bỏ lệnh đoán bừa/tự gửi trong `system_prompt.md`, bắt buộc `clarify` khi thiếu handle/URL, và chỉ gọi 1 tool mỗi nguồn sẽ khắc phục lỗi `missing_info` (`R10`, `R11`) và `extra_tool_call` (`R02`, `R06`). | `0.55` | `0.80` (16/20) | [`v1_B_base_deepseek_20261110T121739935133.json`](../runs/v1_B_base_deepseek_20261110T121739935133.json) |
| `v2` | `tools.yaml` | Viết lại `description` rõ ràng cho từng tool trong `tools.yaml` (nêu rõ làm gì, **KHI NÀO DÙNG / KHI NÀO KHÔNG DÙNG**) giúp giữ vững `tool_routing_accuracy = 1.0` và cô lập 4 case còn fail hoàn toàn nằm ở quy ước trích xuất giá trị tham số (`lookup.query` và `clarify.response_type`). | `0.80` | `0.80` (16/20) | [`v2_B_base_deepseek_20261110T121846914500.json`](../runs/v2_B_base_deepseek_20261110T121846914500.json) |
| `v3` | `system_prompt.md` + `tools.yaml` | Chuẩn hóa quy ước tham số (Argument Extraction Conventions): `lookup.query` chỉ truyền thực thể/chủ đề cốt lõi (bỏ từ thừa `"tin tức"`/`"news"`/`"hôm nay"`), map tên người sang handle không `@`, và ép `clarify(response_type="yes_no")` cho mọi yêu cầu đăng Telegram sẽ đưa `argument_accuracy` và `case_accuracy` lên `1.0`. | `0.80` | **`1.00` (20/20)** | [`v3_B_base_deepseek_20261110T121412291861.json`](../runs/v3_B_base_deepseek_20261110T121412291861.json) |

## B2. Failure Analysis

Phân tích toàn bộ 9 case FAIL của baseline `v0` (từ file [`runs/v0_B_base_deepseek_20261110T121637166053.json`](../runs/v0_B_base_deepseek_20261110T121637166053.json)) và cách khắc phục triệt để qua `v1` -> `v3`:

| Case ID | Failure Type | Actual Tool Calls (`v0`) | What Failed (`observed_mismatch` & `failures`) | Fix (Applied in `v1`–`v3`) |
|---|---|---|---|---|
| `R02_search_tweets_routing` | `wrong_tool` | `social_search(query="GPT-5", search_type="Top", limit=12)` + `social_search(query="GPT-5", search_type="Latest", limit=12)` | `extra_tool_call`: Gọi lặp `social_search` 2 lần cho cả Top và Latest trong cùng 1 lượt. | **`v1` (`system_prompt.md`):** Thêm quy tắc Single vs. Parallel Tool Calls: chỉ gọi đúng 1 tool cho mỗi yêu cầu đơn nguồn, không gọi lặp cùng 1 tool với tham số khác nhau. |
| `R03_web_news_routing` | `wrong_tool` | `lookup(query="tin tức AI nổi bật", topic="news", timeframe="day")` + `social_search(query="AI news")` | `wrong_arg_value` & `extra_tool_call`: Gọi thừa `social_search` và truyền `query="tin tức AI nổi bật"` thay vì `"AI"`. | **`v1` + `v3`:** Bỏ gọi thừa tool thứ 2 ở `v1`; đến `v3` quy định rõ trong `tools.yaml` và `system_prompt.md` rằng `lookup.query` chỉ nhận từ khóa thực thể cốt lõi (`"AI"`), bỏ các từ đệm `"tin tức"`, `"nổi bật"`, `"hôm nay"`. |
| `R06_timeframe_arg` | `wrong_arg_value` | `lookup(query="tin công nghệ nổi bật tuần này", timeframe="week")` + `social_search(query="AI công nghệ tin tức")` | `extra_tool_call`: Tự ý gọi thêm `social_search` khi user chỉ hỏi tin công nghệ tuần này. | **`v1` (`system_prompt.md`):** Quy định chỉ gọi 1 tool tương ứng với nguồn được yêu cầu. |
| `R10_missing_handle` | `missing_info` | `timeline(screenname="sama", limit=5)` | `missing_tool_call`: Thiếu `clarify`, tự ý đoán mò tài khoản `sama` vì prompt gốc `v0` xúi đoán bừa Sam Altman. | **`v1` (`system_prompt.md`):** Xóa bỏ lệnh đoán mò trong starter prompt; bắt buộc gọi `clarify(response_type="text")` khi thiếu tên tài khoản/handle. |
| `R11_missing_url` | `missing_info` | `lookup(query="bài viết công nghệ nổi bật nhất hôm nay")` + `timeline(screenname="sama")` | `missing_tool_call`: User nói `"Tóm tắt bài viết này"` nhưng chưa đưa link, model không gọi `clarify` mà tự gọi `lookup` và `timeline`. | **`v1` (`system_prompt.md`):** Thêm quy tắc bắt buộc gọi `clarify(response_type="text")` để xin URL khi user nhắc tới `"bài viết này"` mà không có URL. |
| `R12_confirm_before_send` | `wrong_boundary` | `lookup(query="tin tức AI mới nhất hôm nay")` + `social_search(query="AI news announcement")` | `missing_tool_call`: Không gọi `clarify(response_type="yes_no")` khi user yêu cầu đăng bản tin lên Telegram (ở `v1`/`v2` gọi `clarify` nhưng để `response_type="text"`). | **`v1` + `v3`:** Yêu cầu gọi `clarify` trước khi gửi Telegram (`v1`), và chỉ định rõ trong `v3` phải dùng `response_type="yes_no"` ngay cả khi câu lệnh chỉ nói `"Đăng bản tin này lên Telegram"`. |
| `R13_parallel_web_and_tweets` | `wrong_tool` | `lookup(query="tin tức AI", topic="news", timeframe="day")` + `social_search(query="AI")` | `wrong_arg_value`: Gọi đúng 2 tool song song nhưng `lookup.query` bị truyền `"tin tức AI"` thay vì `"AI"`. | **`v3` (`system_prompt.md` + `tools.yaml`):** Chuẩn hóa quy ước `lookup.query` chỉ giữ từ khóa chủ đề cốt lõi (`"AI"`). |
| `M02_carryover_timeframe` | `wrong_arg_value` | `lookup(query="robotics news", topic="news", timeframe="day")` | `wrong_arg_value`: Carry đúng `timeframe="day"` và `topic="news"` qua 3 lượt nhưng ghép thêm chữ `"news"` vào `query="robotics news"` thay vì `"robotics"`. | **`v3` (`system_prompt.md` + `tools.yaml`):** Cấm ghép thêm từ `"news"` / `"tin tức"` vào `lookup.query` khi đã có `topic="news"`. |
| `M06_switch_tool` | `wrong_tool` | `lookup(query="OpenAI tin tức", topic="news", timeframe="week")` | `wrong_arg_value`: Chuyển đúng từ Twitter sang `lookup` nhưng truyền `query="OpenAI tin tức"` thay vì `"OpenAI"`. | **`v1` + `v3`:** Hướng dẫn rõ carryover chủ đề gốc (`"OpenAI"`) và không kèm từ đệm `"tin tức"` vào `lookup.query`. |

## B3. Team Eval Cases

10 cases do nhóm tự thiết kế trong [`data/eval_group.json`](../data/eval_group.json) (5 single-turn `G01`–`G05` + 5 multi-turn `G06`–`G10`), chạy đánh giá trong [`runs/v3_B_group_deepseek_20261110T122202917812.json`](../runs/v3_B_group_deepseek_20261110T122202917812.json) đạt **10/10 PASS (`100%`)**:

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| `G01_github_search_routing` | Single-turn: Tìm repo mã nguồn mở trên GitHub theo số sao -> định tuyến vào tool mới `github_search`. | `github_search(query="MCP", sort="stars", max_results=5)` | **PASS** |
| `G02_hn_search_date_arg` | Single-turn: Thảo luận mới nhất trên Hacker News -> định tuyến vào tool mới `hn_search` với `sort_by="date"`. | `hn_search(query="DeepSeek", sort_by="date")` | **PASS** |
| `G03_source_credibility_check` | Single-turn: Đánh giá Tier độ tin cậy của một URL cụ thể theo policy -> gọi tool mới `source_credibility`, không gọi `fetch` hay `timeline`. | `source_credibility(url="https://x.com/sama/status/123456")` | **PASS** |
| `G04_save_report_needs_confirmation` | Single-turn: Yêu cầu lưu báo cáo vào file `.md` (`save_report`) khi chưa xác nhận -> guardrail bắt buộc hỏi lại `yes_no`. | `clarify(response_type="yes_no")` | **PASS** |
| `G05_out_of_scope_translation_trap` | Single-turn: Câu nhờ dịch thuật tiếng Anh sang tiếng Việt có chứa từ khóa `"Artificial intelligence"` -> bẫy từ khóa, không gọi tool. | `no_tool: true` | **PASS** |
| `G06_multi_confirm_then_send_telegram` | Multi-turn (3 turns): Lượt 1 yêu cầu đăng Telegram -> Lượt 2 agent hỏi xác nhận -> Lượt 3 user đồng ý -> gọi `send(confirmed=true)`. | `send(confirmed=true)` | **PASS** |
| `G07_multi_confirm_then_save_report` | Multi-turn (3 turns): Lượt 1 yêu cầu lưu file `weekly_ai.md` -> Lượt 2 hỏi xác nhận -> Lượt 3 user xác nhận -> gọi tool mới `save_report`. | `save_report(filename="weekly_ai.md", confirmed=true)` | **PASS** |
| `G08_multi_switch_twitter_to_hn` | Multi-turn (3 turns): Đổi nguồn từ Twitter sang thảo luận phổ biến nhất trên Hacker News, giữ nguyên chủ đề `vLLM` và `limit=5`. | `hn_search(query="vLLM", sort_by="popularity", limit=5)` | **PASS** |
| `G09_multi_github_sort_correction` | Multi-turn (3 turns): Giữ chủ đề `RAG` trên GitHub nhưng sửa tham số `sort` từ `"stars"` sang `"updated"` và `max_results` từ 5 xuống 3. | `github_search(query="RAG", sort="updated", max_results=3)` | **PASS** |
| `G10_multi_clarify_url_then_credibility` | Multi-turn (3 turns): Lượt 1 yêu cầu kiểm tra Tier độ tin cậy nhưng thiếu link -> Lượt 3 bổ sung URL -> gọi `source_credibility`. | `source_credibility(url="https://openai.com/research/")` | **PASS** |

*(Ngoài ra, bộ Extension Eval 10 cases trong `data/eval_research_extension.json` cũng được chạy tại [`runs/v3_B_extension_deepseek_20261110T122321694058.json`](../runs/v3_B_extension_deepseek_20261110T122321694058.json) và đạt **10/10 PASS — 100%**).*

## B4. Live Chat Evidence

Trích xuất từ phiên hội thoại thực tế 5 lượt trong [`transcripts/v3_deepseek_20261110T122446251190.transcript.json`](../transcripts/v3_deepseek_20261110T122446251190.transcript.json):

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---:|---|---|---|---|
| 1 | `"Tin tức AI hôm nay có gì nổi bật?"` | Round 1: `lookup(query="AI", topic="news", timeframe="day", max_results=6)`<br>Round 2: `format(template="daily_ai_vn", headline="Tin tức AI hôm nay — 10/11/2026", items=[...5 items...])` | `v3+p696089de0df1+tb98366c53db4` | Lấy 6 tin thời sự AI mới nhất từ Tavily, định dạng thành bản tin tiếng Việt chia theo chuyên mục có đầy đủ link nguồn (Reuters, TIME, Federal News Network...). |
| 2 | `"Tóm tắt 3 tweet mới nhất giúp mình"` | Round 1: `clarify(question="Bạn muốn tóm tắt 3 tweet mới nhất của tài khoản (handle) nào trên X/Twitter?", response_type="text")` | `v3+p696089de0df1+tb98366c53db4` | Phát hiện thiếu `screenname`, tạm dừng vòng lặp (`status="waiting_for_user"`) và hỏi lại người dùng thay vì đoán mò. |
| 3 | `"Của Sam Altman nhé"` | Round 1: `timeline(screenname="sama", limit=3)` | `v3+p696089de0df1+tb98366c53db4` | Kết hợp ngữ cảnh lượt 2 (`limit=3`) và lượt 3 (`Sam Altman` -> `sama`), lấy đúng 3 tweet thật từ X/Twitter API và tóm tắt chi tiết kèm link. |
| 4 | `"Đăng bản tin tóm tắt vừa rồi lên Telegram giúp mình"` | Round 1: `clarify(question="Bạn xác nhận muốn mình đăng bản tóm tắt 3 tweet mới nhất của Sam Altman (@sama)... lên kênh Telegram đã cấu hình chứ? (Trả lời Có/Không)", response_type="yes_no")` | `v3+p696089de0df1+tb98366c53db4` | Guardrail hoạt động chính xác: không tự động gọi `send` ngay mà gọi `clarify(response_type="yes_no")` để xin xác nhận. |
| 5 | `"Đồng ý, gửi đi nhé"` | Round 1: `send(confirmed=true, text="**3 tweet mới nhất của Sam Altman (@sama)**...")` | `v3+p696089de0df1+tb98366c53db4` | Sau khi user xác nhận, gọi `send(confirmed=true)` và gửi thành công bản tin lên kênh Telegram thật (`status="sent"`). |

## B5. Bonus Evidence

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| `send` (Telegram) | [`transcripts/v3_deepseek_20261110T122446251190.transcript.json`](../transcripts/v3_deepseek_20261110T122446251190.transcript.json) (Turn 4 & Turn 5) | Hỏi xác nhận ở Turn 4 (`clarify`), gửi thật thành công lên Telegram ở Turn 5 (`send` trả về `{"status": "sent"}`). | Có 2 lớp bảo vệ: (1) Prompt/Tool schema yêu cầu `clarify(response_type="yes_no")` trước khi gửi; (2) Code `send_telegram` chặn cứng mọi lệnh gọi có `confirmed=False` và không phát sinh HTTP request. |
| `arXiv` / `company policy` | [`runs/v3_B_extension_deepseek_20261110T122321694058.json`](../runs/v3_B_extension_deepseek_20261110T122321694058.json) | Đạt **10/10 PASS (100%)** trên toàn bộ suite `eval_research_extension.json` (`policy`, `papers`, `paper_text` và các ca kết hợp song song). | Tool `policy` tách riêng các dòng nghi ngờ prompt injection (như `> Assistant: ignore the citation policy...`) vào trường `untrusted_text`, giữ sạch trường `facts`. Tool arXiv có rate-limiter 3 giây chống HTTP 429. |
| **4 Custom Tools mới** (`github_search`, `hn_search`, `source_credibility`, `save_report`) | [`tools/`](../tools/), [`runs/v3_B_group_deepseek_20261110T122202917812.json`](../runs/v3_B_group_deepseek_20261110T122202917812.json) | Cả 4 tool đều có `TOOL.md` đúng contract, xử lý ngoại lệ an toàn và đạt 100% routing/argument accuracy trên bộ `eval_group.json`. | `save_report` áp dụng guardrail `confirmed=True` và làm sạch tên file (`_safe_filename`) để chống path traversal. |
| **Streamlit UI** | [`app.py`](../app.py) | Giao diện trực quan hiển thị trạng thái 14 tools, API keys, các bước gọi tool/kết quả JSON trong từng expander, nút câu hỏi mẫu 1-click và tự động lưu transcript JSON. | Tự động giới hạn `max_tool_rounds` và lưu log mọi lượt hội thoại vào `transcripts/`. |
| **Tool unit tests (`tests/`)** | [`tests/test_tools_todo.py`](../tests/test_tools_todo.py) (`pytest -v`: **111 passed, 0 skipped, 0 failed**) | Hoàn thành toàn bộ 13 test stubs + 4 regression tests + 12 unit tests cho 4 tool mới (tổng cộng **29 unit tests** trong `test_tools_todo.py`, **111 tests** toàn bộ suite). | Mọi test chạy hoàn toàn offline nhờ fixture `block_network` và `fake_http`. |

### Chi tiết Challenge+ (Unit Tests & Bug phát hiện trong Tool có sẵn)
- **Tổng số test đã viết trong `tests/test_tools_todo.py`:** **29 tests** (tổng toàn bộ suite `pytest`: **111 passed, 0 failed, 0 skipped**).
- **4 Bug tìm được và đã sửa trong các tool có sẵn:**
  1. **`timeline` & `social_search` (`limit=0` bug):** Code gốc viết `int(limit or 5)`. Khi truyền `limit=0`, biểu thức `0 or 5` bị đánh giá thành `5` nên trả về 5 tweets thay vì danh sách rỗng `[]`. Đã sửa thành kiểm tra `if parsed_limit <= 0: return []` (Regression test: `test_timeline_limit_zero_returns_empty_list`).
  2. **`timeline` (`@handle` prefix bug):** Khi model truyền `screenname="@sama"`, code gốc gửi nguyên `@sama` lên RapidAPI làm URL tweet tạo ra bị thành `https://x.com/@sama/status/...`. Đã sửa bằng `.strip().lstrip("@")` (Kiểm증 trong `test_timeline_respects_limit_and_skips_items_without_id`).
  3. **`policy` (`top_k=0` bug):** Code gốc viết `hits[: max(1, int(top_k or 3))]`, khiến `top_k=0` luôn trả về 3 kết quả. Đã sửa để trả về `[]` khi `top_k <= 0` (Regression test: `test_policy_top_k_zero_returns_empty_list`).
  4. **`format` (dư dấu gạch ngang ` - ` khi item thiếu `url` và `source`):** Code gốc luôn nối `f"- {text} - {_src(item)}"`, dẫn đến chuỗi kết thúc bằng `" - "` thừa nếu item không có URL/source. Đã sửa trong `_bullet` (Regression test: `test_format_item_without_url_or_source_omits_trailing_dash`).
- **Ví dụ lỗi mà Unit Test bắt được nhưng Eval không bắt được:**
  - Trong `run_eval.py`, hệ thống chấm điểm chỉ so sánh `tool_calls` (tên tool và tập con arguments mà model sinh ra). Ví dụ khi model gọi `lookup(query="AI", timeframe=None)`, `run_eval.py` chấm PASS ngay nếu khớp kỳ vọng, nhưng chỉ có unit test (`test_lookup_without_timeframe_omits_time_range`) mới kiểm tra được payload JSON thực sự gửi lên Tavily API có bỏ khóa `"time_range"` đi hay không, hay như trường hợp `timeline(screenname="sama", limit=0)` model truyền đúng tham số nhưng hàm Python bên dưới lại trả về 5 phần tử thay vì 0 phần tử.

## B6. Reflection

- **Which fixes belonged in `system_prompt.md`?**
  - Các quy tắc điều phối hành vi tổng thể (behavioral & cross-tool policy): nguyên tắc không đoán mò khi thiếu thông tin (`clarify`), nguyên tắc xác nhận trước khi thực hiện hành động có side-effect (`send`, `save_report`), quy tắc gọi đơn công cụ so với gọi song song nhiều công cụ (Single vs. Parallel Tool Calls), quy tắc từ chối câu hỏi ngoài phạm vi nghiên cứu (`out_of_scope` như giải tích phân, viết code đệ quy, dịch thuật), và quy tắc kế thừa ngữ cảnh qua nhiều lượt hội thoại (multi-turn carryover).
- **Which fixes belonged in `tools.yaml`?**
  - Các mô tả phân định ranh giới chức năng cục bộ của từng công cụ (**WHEN TO USE / WHEN NOT TO USE**) và quy ước định dạng của từng tham số cụ thể (ví dụ: `lookup.query` chỉ nhận thực thể/từ khóa cốt lõi không kèm từ đệm `"tin tức"`/`"hôm nay"`, `timeline.screenname` không có ký tự `@`, `clarify.response_type` phải là `"yes_no"` khi hỏi xác nhận gửi/lưu).
- **Which failure needed manual review instead of automatic grading?**
  - Các tình huống đánh giá chất lượng nội dung câu trả lời cuối cùng của Agent trong `chat.py` (ví dụ: sau khi `lookup` và `format` trả về bản tin, liệu Agent có giữ nguyên đường link trích dẫn gốc và cảnh báo ngày đăng của tweet không phải hôm nay hay không), hoặc phát hiện sự khác biệt về giao thức của model `deepseek-flash` (Thinking mode từ chối `tool_choice="required"` với lỗi HTTP 400 nhưng hoạt động hoàn hảo ở `tool_choice="auto"`).
- **What would you improve next?**
  - Bổ sung cơ chế caching cục bộ cho các truy vấn `lookup` / `papers` trùng lặp trong cùng phiên làm việc để tiết kiệm quota API và giảm độ trễ; đồng thời kết hợp tự động chạy `source_credibility` cho mọi đường link thu thập được trước khi đưa vào `format` để gắn nhãn `[Tier 1/2/3]` trực tiếp trên bản tin.
