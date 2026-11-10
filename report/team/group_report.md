# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster [`report/team/poster.html`](poster.html) hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: **K5-L3A-DAY03 — Nguyễn Văn Nhi (`2A202603697`)** (Làm cá nhân)
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md) và báo cáo cá nhân [`report/team/2A202603697_NguyenVanNhi.md`](2A202603697_NguyenVanNhi.md)
- Provider/model dùng cho v0–v3: **`deepseek` / `deepseek-flash` (DeepSeek-V4.1-Flash)** (có hỗ trợ đầy đủ cả `openrouter`, `openai`, `anthropic`, `gemini`, `ollama`)

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

**AI & Technology Research Agent** là trợ lý nghiên cứu công nghệ đa nguồn dựa trên bằng chứng (evidence-driven): tự động định tuyến và tra cứu tin tức thời sự (Tavily), thảo luận mạng xã hội Twitter/X (RapidAPI) & Hacker News (Algolia), kho mã nguồn mở GitHub, bài báo khoa học arXiv, quy định nội bộ công ty (`company_policy`), đánh giá cấp độ tin cậy của nguồn tin (`Tier 1/2/3`), tổng hợp thành bản tin Markdown chuẩn hóa và xuất file hoặc đăng lên kênh Telegram khi có sự xác nhận rõ ràng của người dùng.

**Cách chạy UI:**

- Đã bổ sung `streamlit>=1.30.0` vào [`starter_v0/requirements.txt`](../../starter_v0/requirements.txt).
- Chạy từ thư mục `starter_v0/`:
  ```bash
  cd starter_v0
  streamlit run app.py
  ```

**Link dùng thử (deploy):**

> Mở public link bằng Cloudflare Tunnel (`cloudflared tunnel --url http://localhost:8501`) hoặc chạy trực tiếp local.
>
> URL: `https://editions-delivers-rich-sake.trycloudflare.com` (Local: `http://localhost:8501`, Poster trực quan: [`report/team/poster.html`](poster.html))

### A2. Tool agent có

Agent được trang bị tổng cộng **14 công cụ** (6 Core + 4 Optional có sẵn + **4 Tool mới do nhóm tự phát triển**):

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

### A3. Câu hỏi mẫu để thử

1. **Tra cứu tin tức & tổng hợp tự động:** `"Tin tức AI hôm nay có gì nổi bật?"`
2. **Tìm kiếm mã nguồn mở (Tool mới `github_search`):** `"Tìm giúp mình 5 repo GitHub nhiều sao nhất về MCP"`
3. **Thảo luận cộng đồng kỹ thuật (Tool mới `hn_search`):** `"Cộng đồng Hacker News mới nhất đang thảo luận gì về DeepSeek?"`
4. **Kiểm tra độ tin cậy nguồn trích dẫn (Tool mới `source_credibility`):** `"Đánh giá độ tin cậy (Tier mấy theo policy) của nguồn này: https://x.com/sama/status/123456"`
5. **Kiểm tra hỏi lại khi thiếu thông tin & guardrail xác nhận:** `"Tóm tắt 3 tweet mới nhất giúp mình"` -> trả lời `"Của Sam Altman nhé"` -> `"Đăng bản tin vừa rồi lên Telegram giúp mình"`.

## 3. Giải pháp

- **Tối ưu `starter_v0/artifacts/system_prompt.md`:**
  - Xóa bỏ toàn bộ các chỉ dẫn xấu cố ý trong bản `starter_v0` (như đoán mò `@sama` khi thiếu handle, gửi thẳng lên Telegram không cần hỏi, ép hoàn thành trong 1 bước).
  - Thiết lập bảng quy tắc định tuyến rõ ràng (**Tool Routing Rules**) cho cả 14 công cụ, quy tắc gọi đơn công cụ vs. gọi song song (**Single vs. Parallel Tool Calls**), quy tắc trích xuất tham số (**Argument Extraction Conventions**), ranh giới hỏi lại & xác nhận (**Clarification & Confirmation Boundaries**), kế thừa ngữ cảnh đa lượt (**Multi-turn Context Carryover**), và từ chối câu hỏi ngoài phạm vi (**Out-of-Scope & Conversational Queries**).
- **Tối ưu `starter_v0/artifacts/tools.yaml`:**
  - Viết lại toàn bộ `description` của từng tool theo cấu trúc: chức năng chính, **WHEN TO USE** (khi nào dùng), **WHEN NOT TO USE** (khi nào không dùng).
  - Chuẩn hóa mô tả của từng tham số: `lookup.query` chỉ nhận thực thể/chủ đề cốt lõi (không kèm từ đệm `"tin tức"`, `"news"`, `"hôm nay"`), `timeline.screenname` không có ký tự `@`, `clarify.response_type` bắt buộc dùng `"yes_no"` khi xin phép gửi Telegram hoặc lưu file.
- **Phát triển 4 Tool mới trong `starter_v0/tools/`:**
  1. [`github_search`](../../starter_v0/tools/github_search/tool.py): Tìm kiếm repository trên GitHub REST API (`sort="stars"|"updated"|"forks"`), gọi khi người dùng tìm mã nguồn mở, thư viện hoặc project GitHub.
  2. [`hn_search`](../../starter_v0/tools/hn_search/tool.py): Tìm kiếm bài đăng thảo luận kỹ thuật trên Hacker News Algolia API (`sort_by="popularity"|"date"`), gọi khi người dùng hỏi ý kiến cộng đồng HN/YCombinator.
  3. [`source_credibility`](../../starter_v0/tools/source_credibility/tool.py): Phân loại cấp độ tin cậy của URL (`Tier 1`, `Tier 2`, `Tier 3`) theo đúng chuẩn `source_citation.md` của công ty, gọi khi người dùng muốn đánh giá độ uy tín nguồn tin.
  4. [`save_report`](../../starter_v0/tools/save_report/tool.py): Lưu báo cáo Markdown vào `saved_reports/` với chốt chặn an toàn `confirmed=True` và chống path traversal (`_safe_filename`), gọi sau khi người dùng đã xác nhận đồng ý lưu file.

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ [`starter_v0/artifacts/version_log.csv`](../../starter_v0/artifacts/version_log.csv) và [`starter_v0/runs/*.json`](../../starter_v0/runs/). Tất cả các run đều hợp lệ tuyệt đối (`provider_error_cases == 0` và `measured_cases == total_cases == 20`).

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| `v0` | `baseline` | Đo hành vi baseline của `starter_v0` với model `deepseek-flash` trước khi tối ưu prompt và tool declarations (`routing=0.70`, `arg=0.55`, `multiturn=0.6667`). | — | `0.55` (11/20) | [`v0_B_base_deepseek_20261110T121637166053.json`](../../starter_v0/runs/v0_B_base_deepseek_20261110T121637166053.json) |
| `v1` | `system_prompt.md` | Loại bỏ lệnh đoán bừa/tự gửi trong `system_prompt.md`, bắt buộc `clarify` khi thiếu handle/URL, và chỉ gọi 1 tool mỗi nguồn sẽ khắc phục lỗi `missing_info` (`R10`, `R11`) và `extra_tool_call` (`R02`, `R06`). | `0.55` | `0.80` (16/20) | [`v1_B_base_deepseek_20261110T121739935133.json`](../../starter_v0/runs/v1_B_base_deepseek_20261110T121739935133.json) |
| `v2` | `tools.yaml` | Viết lại `description` rõ ràng cho từng tool trong `tools.yaml` (nêu rõ làm gì, **KHI NÀO DÙNG / KHI NÀO KHÔNG DÙNG**) giúp giữ vững `tool_routing_accuracy = 1.0` và cô lập 4 case còn fail hoàn toàn nằm ở quy ước trích xuất giá trị tham số (`lookup.query` và `clarify.response_type`). | `0.80` | `0.80` (16/20) | [`v2_B_base_deepseek_20261110T121846914500.json`](../../starter_v0/runs/v2_B_base_deepseek_20261110T121846914500.json) |
| `v3` | `system_prompt.md` + `tools.yaml` | Chuẩn hóa quy ước tham số (Argument Extraction Conventions): `lookup.query` chỉ truyền thực thể/chủ đề cốt lõi (bỏ từ thừa `"tin tức"`/`"news"`/`"hôm nay"`), map tên người sang handle không `@`, và ép `clarify(response_type="yes_no")` cho mọi yêu cầu đăng Telegram sẽ đưa `argument_accuracy` và `case_accuracy` lên `1.0`. | `0.80` | **`1.00` (20/20)** | [`v3_B_base_deepseek_20261110T121412291861.json`](../../starter_v0/runs/v3_B_base_deepseek_20261110T121412291861.json) |

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong [`starter_v0/runs/v0_B_base_deepseek_20261110T121637166053.json`](../../starter_v0/runs/v0_B_base_deepseek_20261110T121637166053.json) (toàn bộ 9/9 case FAIL của `v0`):

| Case ID | Failure Type | Actual Tool Calls (`v0`) | What Failed | Fix |
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

### B3. Team Eval Cases

Liệt kê đúng 10 case trong [`starter_v0/data/eval_group.json`](../../starter_v0/data/eval_group.json) (5 single turn `G01`–`G05` + 5 multi turn `G06`–`G10`), chạy đánh giá tại [`starter_v0/runs/v3_B_group_deepseek_20261110T122202917812.json`](../../starter_v0/runs/v3_B_group_deepseek_20261110T122202917812.json) đạt **10/10 PASS (`100%`)**:

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

*(Ngoài ra, bộ Extension Eval 10 cases trong `starter_v0/data/eval_research_extension.json` cũng được chạy tại [`starter_v0/runs/v3_B_extension_deepseek_20261110T122321694058.json`](../../starter_v0/runs/v3_B_extension_deepseek_20261110T122321694058.json) và đạt **10/10 PASS — 100%**).*

### B4. Live Chat Evidence

Lấy từ [`starter_v0/transcripts/v3_deepseek_20261110T122446251190.transcript.json`](../../starter_v0/transcripts/v3_deepseek_20261110T122446251190.transcript.json) (và các phiên live UI trong [`starter_v0/transcripts/`](../../starter_v0/transcripts/)):

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---:|---|---|---|---|
| 1 | `"Tin tức AI hôm nay có gì nổi bật?"` | Round 1: `lookup(query="AI", topic="news", timeframe="day", max_results=6)`<br>Round 2: `format(template="daily_ai_vn", headline="Tin tức AI hôm nay — 10/11/2026", items=[...5 items...])` | `v3+p696089de0df1+tb98366c53db4` | Lấy 6 tin thời sự AI mới nhất từ Tavily, định dạng thành bản tin tiếng Việt chia theo chuyên mục có đầy đủ link nguồn (Reuters, TIME, Federal News Network...). |
| 2 | `"Tóm tắt 3 tweet mới nhất giúp mình"` | Round 1: `clarify(question="Bạn muốn tóm tắt 3 tweet mới nhất của tài khoản (handle) nào trên X/Twitter?", response_type="text")` | `v3+p696089de0df1+tb98366c53db4` | Phát hiện thiếu `screenname`, tạm dừng vòng lặp (`status="waiting_for_user"`) và hỏi lại người dùng thay vì đoán mò. |
| 3 | `"Của Sam Altman nhé"` | Round 1: `timeline(screenname="sama", limit=3)` | `v3+p696089de0df1+tb98366c53db4` | Kết hợp ngữ cảnh lượt 2 (`limit=3`) và lượt 3 (`Sam Altman` -> `sama`), lấy đúng 3 tweet thật từ X/Twitter API và tóm tắt chi tiết kèm link. |
| 4 | `"Đăng bản tin tóm tắt vừa rồi lên Telegram giúp mình"` | Round 1: `clarify(question="Bạn xác nhận muốn mình đăng bản tóm tắt 3 tweet mới nhất của Sam Altman (@sama)... lên kênh Telegram đã cấu hình chứ? (Trả lời Có/Không)", response_type="yes_no")` | `v3+p696089de0df1+tb98366c53db4` | Guardrail hoạt động chính xác: không tự động gọi `send` ngay mà gọi `clarify(response_type="yes_no")` để xin xác nhận. |
| 5 | `"Đồng ý, gửi đi nhé"` | Round 1: `send(confirmed=true, text="**3 tweet mới nhất của Sam Altman (@sama)**...")` | `v3+p696089de0df1+tb98366c53db4` | Sau khi user xác nhận, gọi `send(confirmed=true)` và gửi thành công bản tin lên kênh Telegram thật (`status="sent"`). |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/github_search/`, `tools/hn_search/`, `tools/source_credibility/`, `tools/save_report/`) | [`starter_v0/tools/`](../../starter_v0/tools/), [`starter_v0/tools/__init__.py`](../../starter_v0/tools/__init__.py), [`starter_v0/artifacts/tools.yaml`](../../starter_v0/artifacts/tools.yaml) | Cả 4 tool mới đều có `TOOL.md` đúng contract, tự đóng gói độc lập trong `tool.py`, đăng ký đồng bộ và đạt 100% routing/arg accuracy trên `eval_group.json`. | Mọi tool đều bắt `requests.RequestException` để trả về `{"error": ...}` thay vì raise exception; `save_report` có guardrail `confirmed=True` và lọc path traversal (`_safe_filename`). |
| Unit test tool mới (≥ 3 test/tool) | [`starter_v0/tests/test_tools_todo.py`](../../starter_v0/tests/test_tools_todo.py) (`pytest`: **111 passed, 0 failed, 0 skipped**) | Viết đủ 12 unit test cho 4 tool mới (3 test/tool: happy path, bad input/clamping, network/boundary error) + hoàn thành toàn bộ 13 stub + 4 regression tests. | Toàn bộ unit test chạy offline 100% nhờ fixture `block_network` và `fake_http` trong `conftest.py`. |
| UI (lệnh chạy + link dùng thử) | [`starter_v0/app.py`](../../starter_v0/app.py), [`starter_v0/requirements.txt`](../../starter_v0/requirements.txt), [`starter_v0/transcripts/v3_ui_deepseek_20261110T141722493242.transcript.json`](../../starter_v0/transcripts/v3_ui_deepseek_20261110T141722493242.transcript.json) | Giao diện Streamlit hiển thị trạng thái 14 tools, danh sách API keys, expander xem trực tiếp từng bước gọi tool & JSON output, nút câu hỏi mẫu 1-click và xuất transcript tự động. | Giới hạn `max_tool_rounds` chống vòng lặp vô hạn, hiển thị minh bạch mọi lỗi tool nếu có và tự động lưu log vào `starter_v0/transcripts/`. |

**Tool unit tests:** Đã viết tổng cộng **29 unit tests** trong `starter_v0/tests/test_tools_todo.py` (nâng tổng số test toàn bộ suite `pytest` lên **111 passed, 0 failed, 0 skipped**).
- **Ví dụ lỗi mà Unit Test bắt được nhưng Eval không bắt được:** Trong `run_eval.py`, hệ thống chấm điểm chỉ so sánh `tool_calls` (tên tool và tập con arguments mà model sinh ra). Ví dụ khi model gọi `lookup(query="AI", timeframe=None)`, `run_eval.py` chấm PASS ngay nếu khớp kỳ vọng, nhưng chỉ có unit test (`test_lookup_without_timeframe_omits_time_range`) mới kiểm tra được payload JSON thực sự gửi lên Tavily API có bỏ khóa `"time_range"` đi hay không; hoặc khi model gọi `timeline(screenname="sama", limit=0)` thì chỉ có unit test (`test_timeline_limit_zero_returns_empty_list`) mới phát hiện ra lỗi `int(limit or 5)` biến `0` thành `5` ở tầng code Python.

### B5. Bonus Evidence

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | *(Không thực hiện)* | — | — |
| **Hơn 3 tool mới (≥ 4 tool do nhóm tự viết)** (+3 điểm) | [`starter_v0/tools/github_search/`](../../starter_v0/tools/github_search/), [`starter_v0/tools/hn_search/`](../../starter_v0/tools/hn_search/), [`starter_v0/tools/source_credibility/`](../../starter_v0/tools/source_credibility/), [`starter_v0/tools/save_report/`](../../starter_v0/tools/save_report/), [`starter_v0/runs/v3_B_group_deepseek_20261110T122202917812.json`](../../starter_v0/runs/v3_B_group_deepseek_20261110T122202917812.json) | 4 tool mới hoàn toàn (`github_search`, `hn_search`, `source_credibility`, `save_report`), mỗi tool có `TOOL.md`, đăng ký đầy đủ, ≥ 3 unit test và có eval cases (`G01`–`G04`, `G07`–`G10`) route tới đạt 100% PASS. | Kiểm soát chặt input (clamp `max_results`/`limit`, validate enum `sort`/`sort_by`, chặn path traversal và yêu cầu `confirmed=True` ở `save_report`). |
| **`send` gửi thật lên Telegram sau xác nhận** (+2 điểm) | [`starter_v0/transcripts/v3_deepseek_20261110T122446251190.transcript.json`](../../starter_v0/transcripts/v3_deepseek_20261110T122446251190.transcript.json) (Turn 4 & Turn 5) | Luồng chuẩn xác: Turn 4 user yêu cầu đăng -> Agent gọi `clarify(response_type="yes_no")` -> Turn 5 user xác nhận `"Đồng ý, gửi đi nhé"` -> Agent gọi `send(confirmed=true)` -> trả về `{"status": "sent"}` trên kênh Telegram. | Bảo vệ 2 lớp: (1) Prompt/Schema bắt buộc hỏi `clarify(response_type="yes_no")` trước; (2) Code `send_telegram` chặn cứng mọi lệnh gọi có `confirmed=False` mà không gọi mạng. |
| **Test challenge (0 skipped + regression tests)** (+1 điểm) | [`starter_v0/tests/test_tools_todo.py`](../../starter_v0/tests/test_tools_todo.py) (`pytest`: **111 passed, 0 skipped, 0 failed**) | Hoàn thành toàn bộ 13 stub có sẵn + 12 test cho 4 tool mới + **4 regression tests** cho 4 bug phát hiện trong các tool gốc của starter. | Giữ toàn bộ 111 tests chạy offline nhanh (~0.3s) và kiểm tra chặt chẽ cả request gửi đi lẫn kết quả trả về. |

**Chi tiết Test Challenge — 4 Bug tìm được trong tool có sẵn, cách sửa và regression test tương ứng:**
1. **`timeline` & `social_search` (`limit=0` bug):** Code gốc trong [`starter_v0/tools/timeline/tool.py`](../../starter_v0/tools/timeline/tool.py) và [`starter_v0/tools/social_search/tool.py`](../../starter_v0/tools/social_search/tool.py) viết `int(limit or 5)`. Khi truyền `limit=0`, biểu thức `0 or 5` bị đánh giá thành `5` nên trả về 5 tweets thay vì danh sách rỗng `[]`. **Cách sửa:** Kiểm tra `if limit is not None and int(limit) <= 0: return []`. **Regression test:** `test_timeline_limit_zero_returns_empty_list`.
2. **`timeline` (`@handle` prefix bug):** Khi model truyền `screenname="@sama"`, code gốc giữ nguyên ký tự `@` làm URL trả về bị lỗi thành `https://x.com/@sama/status/...`. **Cách sửa:** Chuẩn hóa `clean_handle = screenname.strip().lstrip("@")`. **Regression test:** `test_timeline_respects_limit_and_skips_items_without_id`.
3. **`policy` (`top_k=0` bug):** Code gốc trong [`starter_v0/tools/policy/tool.py`](../../starter_v0/tools/policy/tool.py) viết `hits[: max(1, int(top_k or 3))]`, khiến `top_k=0` luôn trả về kết quả thay vì `[]`. **Cách sửa:** Trả về `[]` ngay khi `int(top_k) <= 0`. **Regression test:** `test_policy_top_k_zero_returns_empty_list`.
4. **`format` (dư dấu gạch ngang ` - ` khi item thiếu `url` và `source`):** Code gốc trong [`starter_v0/tools/format/tool.py`](../../starter_v0/tools/format/tool.py) luôn nối `f"- {text} - {_src(item)}"`, dẫn đến chuỗi kết thúc bằng `" - "` thừa nếu item không có URL/source. **Cách sửa:** Chỉ nối ` - {src}` khi `_src(item)` không rỗng. **Regression test:** `test_format_item_without_url_or_source_omits_trailing_dash`.

### B7. Small Local Model Challenge (bonus)

*(Nhóm tập trung hoàn thiện tối đa chất lượng 3 hạng mục Bonus: 4 Custom Tools mới, Gửi Telegram thật sau xác nhận, và Test Challenge 111 passed / 0 skipped + 4 Regression Bugs).*

## 5. Khó khăn và cách xử lý

- **Khó khăn 1 — Tương thích giao thức `tool_choice="required"` với chế độ Thinking của model:**
  - Khi chạy preflight và eval với `deepseek-flash` (hoặc qua OpenRouter), các case có `force_tool=True` trong `eval_base.json` gửi `tool_choice="required"`. API của DeepSeek trả lỗi HTTP 400 (`Thinking mode does not support tool_choice="required"`).
  - **Cách xử lý:** Trong [`starter_v0/providers/deepseek_provider.py`](../../starter_v0/providers/deepseek_provider.py) và [`starter_v0/providers/openrouter_provider.py`](../../starter_v0/providers/openrouter_provider.py), tự động ánh xạ `tool_choice="required"` sang `"auto"` đối với dòng model DeepSeek, giúp toàn bộ 20/20 case chạy mượt mà với `provider_error_cases == 0`.
- **Khó khăn 2 — Phân biệt lỗi chọn sai tool (`wrong_tool`) với lỗi truyền thừa từ khóa trong tham số (`wrong_arg_value`):**
  - Ở vòng `v1` và `v2`, dù `tool_routing_accuracy` đã đạt tuyệt đối `1.00`, vẫn còn 4 case fail (`R03`, `R13`, `M02`, `M06`) do model truyền `lookup(query="tin tức AI")` hoặc `lookup(query="robotics news")` thay vì chỉ truyền thực thể cốt lõi `"AI"` / `"robotics"`.
  - **Cách xử lý:** Ở vòng `v3`, bổ sung quy ước **Argument Extraction Conventions** vào cả `system_prompt.md` và mô tả tham số `lookup.query` trong `tools.yaml`, đưa `case_accuracy` từ `0.80` lên `1.00` (20/20).
- **Khó khăn 3 — Đồng bộ đề cập nhật từ giảng viên khi đã có 9 commit local:**
  - Khi giảng viên cập nhật cấu trúc repo (thêm `TEAM.md`, `RUBRIC.md`, `SUBMISSION.md`, chuyển `REPORT.md` sang `report/team/group_report.md`), nhánh local đang ahead 9 commits.
  - **Cách xử lý:** Thực hiện `git merge origin/main` để bảo toàn nguyên vẹn lịch sử 9 commit kỹ thuật ban đầu đồng thời chuyển đổi báo cáo và bổ sung đầy đủ các file theo chuẩn mới mà không cần force-push.

## 6. Tổng hợp đóng góp

Bài lab được thực hiện cá nhân bởi **Nguyễn Văn Nhi (`2A202603697`)** — phụ trách 100% các hạng mục từ thiết lập provider, chạy baseline `v0`, tối ưu `v1`–`v3`, xây dựng 4 tool mới, viết 29 unit tests, thiết kế 10 case `eval_group.json`, xây dựng Streamlit UI `app.py`, chạy live chat gửi Telegram thật, và viết báo cáo.

Chi tiết đóng góp và danh sách commit nằm trong [TEAM.md](../../TEAM.md) và báo cáo cá nhân [`report/team/2A202603697_NguyenVanNhi.md`](2A202603697_NguyenVanNhi.md).

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- **Fix nào thuộc `system_prompt.md`?**
  - Các quy tắc điều phối hành vi tổng thể (behavioral & cross-tool policy): nguyên tắc không đoán mò khi thiếu thông tin (`clarify`), nguyên tắc xác nhận trước khi thực hiện hành động có side-effect (`send`, `save_report`), quy tắc gọi đơn công cụ so với gọi song song nhiều công cụ (Single vs. Parallel Tool Calls), quy tắc từ chối câu hỏi ngoài phạm vi nghiên cứu (`out_of_scope` như giải tích phân, viết code đệ quy, dịch thuật), và quy tắc kế thừa ngữ cảnh qua nhiều lượt hội thoại (multi-turn carryover).
- **Fix nào thuộc `tools.yaml`?**
  - Các mô tả phân định ranh giới chức năng cục bộ của từng công cụ (**WHEN TO USE / WHEN NOT TO USE**) và quy ước định dạng của từng tham số cụ thể (ví dụ: `lookup.query` chỉ nhận thực thể/từ khóa cốt lõi không kèm từ đệm `"tin tức"`/`"hôm nay"`, `timeline.screenname` không có ký tự `@`, `clarify.response_type` phải là `"yes_no"` khi hỏi xác nhận gửi/lưu).
- **Failure nào cần review thủ công thay vì chấm tự động?**
  - Các tình huống đánh giá chất lượng nội dung câu trả lời tổng hợp cuối cùng của Agent trong `chat.py` (ví dụ: sau khi `lookup` và `format` trả về bản tin, liệu Agent có giữ nguyên đường link trích dẫn gốc, không bịa đặt số liệu và cảnh báo ngày đăng của tweet không phải hôm nay hay không), hoặc kiểm tra xem nội dung tin nhắn gửi lên Telegram có trình bày rõ ràng, dễ đọc cho người dùng cuối hay không.
- **Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?**
  - Thử nghiệm giả thuyết `v4-local` trên các model nhỏ chạy qua Ollama (`qwen2.5:7b` và `llama3.1:8b`): rút gọn độ dài của `system_prompt.md` xuống dưới 40 dòng và đưa các quy ước rút trích tham số quan trọng nhất lên câu đầu tiên của từng `description` trong `tools.yaml` để kiểm chứng mức độ cải thiện `argument_accuracy` trên các model ≤ 8B.

## 8. Tài liệu tham khảo

- Tài liệu hướng dẫn Lab Day 03: [README.md](../../README.md), [CHECKPOINTS.md](../../CHECKPOINTS.md), [RUBRIC.md](../../RUBRIC.md), [RULES.md](../../RULES.md), [SUBMISSION.md](../../SUBMISSION.md), [docs/TOOL-SETUP.md](../../docs/TOOL-SETUP.md).
- Tavily Search API Documentation (`https://docs.tavily.com`).
- Firecrawl API Documentation (`https://docs.firecrawl.dev`).
- GitHub REST API — Search Repositories (`https://docs.github.com/en/rest/search/search#search-repositories`).
- Hacker News Algolia Search API (`https://hn.algolia.com/api`).
- DeepSeek API — Function Calling & Tool Choice Guide (`https://api-docs.deepseek.com/guides/function_calling`).
