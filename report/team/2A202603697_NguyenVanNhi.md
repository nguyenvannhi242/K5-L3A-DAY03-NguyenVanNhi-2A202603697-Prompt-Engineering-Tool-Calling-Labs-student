# Báo cáo cá nhân — Nguyễn Văn Nhi - 2A202603697

## 1. Thông tin thành viên

- Họ tên: **Nguyễn Văn Nhi**
- MSSV: **`2A202603697`**
- Email: `nguyenvannhi224@gmail.com`
- GitHub: `nguyenvannhi242` (`hagasei`)
- Lớp: `K5-L3A`

## 2. Phần việc phụ trách

Thực hiện cá nhân (100% khối lượng bài Lab Day 03), bao gồm toàn bộ 5 Checkpoints (CP1–CP5) và 3 hạng mục Bonus:

1. **CP1 — Setup & Baseline `v0`:** Cấu hình `.env`, tích hợp adapter `deepseek-flash` & `openrouter`, chạy baseline `v0` trên bộ `eval_base.json` (20 cases), phân tích chi tiết toàn bộ 9 case FAIL và ghi nhận vào `version_log.csv` + bảng B2.
2. **CP2 — Tối ưu Prompt & Tool Declarations (`v1` -> `v3`):** Thực hiện 3 vòng tối ưu theo đúng phương pháp 1 giả thuyết/vòng:
   - `v1`: Loại bỏ chỉ dẫn xấu trong `system_prompt.md`, thiết lập rule routing và boundary `clarify` -> tăng `case_accuracy` từ `0.55` lên `0.80` (`tool_routing_accuracy` đạt `1.00`).
   - `v2`: Viết lại toàn bộ `description` trong `tools.yaml` (**WHEN TO USE / WHEN NOT TO USE**), giữ vững `tool_routing_accuracy = 1.00` và cô lập 4 lỗi còn lại đều thuộc `wrong_arg_value`.
   - `v3`: Chuẩn hóa quy ước trích xuất tham số (**Argument Extraction Conventions**) trong `system_prompt.md` và `tools.yaml` -> đưa `case_accuracy`, `tool_routing_accuracy`, `argument_accuracy`, `multiturn_accuracy` đạt tuyệt đối **`1.00` (20/20)**.
3. **CP3 — Phát triển 4 Tool mới & Unit Test Suite (Bonus >3 tools + Test Challenge):**
   - Thiết kế và cài đặt 4 công cụ mới: `github_search`, `hn_search`, `source_credibility`, `save_report` (kèm `TOOL.md` đúng contract, đăng ký trong `tools/__init__.py` và `artifacts/tools.yaml`).
   - Hoàn thiện toàn bộ 13 test stubs trong `tests/test_tools_todo.py`, viết thêm 12 unit tests cho 4 tool mới và 4 regression tests cho 4 bug phát hiện trong các tool có sẵn -> đạt **`111 passed, 0 failed, 0 skipped`**.
4. **CP4 — Thiết kế 10 Case Eval Nhóm (`eval_group.json`):** Viết 5 single-turn (`G01`–`G05`) và 5 multi-turn (`G06`–`G10`) kiểm tra định tuyến vào cả 4 tool mới, guardrail xác nhận trước khi gửi/lưu, bẫy dịch thuật ngoài phạm vi và đổi công cụ đa lượt -> chạy `--suite group` đạt **10/10 PASS (`100%`)** (đồng thời chạy `--suite extension` đạt **10/10 PASS**).
5. **CP5 — Xây dựng UI Streamlit, Live Chat (gửi Telegram thật) & Báo cáo:**
   - Xây dựng giao diện `starter_v0/app.py` bằng Streamlit, mở public link qua Cloudflare Tunnel, tạo poster trực quan `report/team/poster.html`.
   - Chạy hội thoại nhiều lượt thực tế (`chat.py` & UI), kiểm chứng luồng hỏi lại khi thiếu thông tin và xác nhận trước khi gửi tin nhắn thật lên kênh Telegram (`status="sent"`).
   - Hoàn thiện báo cáo nhóm `report/team/group_report.md`, `TEAM.md` và báo cáo cá nhân `report/team/2A202603697_NguyenVanNhi.md`.

## 3. Đóng góp cụ thể

- **Tối ưu Prompt & Schema (`starter_v0/artifacts/system_prompt.md`, `starter_v0/artifacts/tools.yaml`):**
  - Xóa bỏ các hướng dẫn gây lỗi cố ý của starter (`@sama` mặc định, tự gửi Telegram, ép gọi 1 bước).
  - Bổ sung quy tắc phân biệt rõ ràng giữa `timeline` (bài đăng của 1 tài khoản), `social_search` (bài đăng theo chủ đề trên X), `lookup` (báo chí/tin tức web), `fetch` (đọc nội dung 1 URL cụ thể), `papers`/`paper_text` (bài báo arXiv), `policy` (quy định nội bộ), và 4 công cụ mới (`github_search`, `hn_search`, `source_credibility`, `save_report`).
- **4 Công cụ mới tự phát triển (`starter_v0/tools/`):**
  1. `github_search` (`starter_v0/tools/github_search/tool.py`): Tìm kiếm repository mã nguồn mở qua GitHub REST API với sắp xếp `stars`/`updated`/`forks` và xử lý lỗi mạng an toàn.
  2. `hn_search` (`starter_v0/tools/hn_search/tool.py`): Tìm kiếm thảo luận cộng đồng lập trình viên trên Hacker News (Algolia API) theo `popularity` hoặc `date`.
  3. `source_credibility` (`starter_v0/tools/source_credibility/tool.py`): Đánh giá tự động cấp độ tin cậy nguồn trích dẫn (`Tier 1`, `Tier 2`, `Tier 3`) dựa trên tên miền/đường dẫn theo đúng chuẩn `company_policy/source_citation.md`.
  4. `save_report` (`starter_v0/tools/save_report/tool.py`): Xuất báo cáo Markdown ra thư mục `saved_reports/` với chốt chặn bắt buộc `confirmed=True` và hàm `_safe_filename` chống tấn công path traversal.
- **Phát hiện & Sửa 4 Bug trong các Tool có sẵn (kèm Regression Tests):**
  1. Sửa lỗi `int(limit or 5)` biến `limit=0` thành `5` trong `timeline/tool.py` và `social_search/tool.py`.
  2. Sửa lỗi giữ nguyên tiền tố `@` trong `screenname` của `timeline/tool.py` làm hỏng URL tweet.
  3. Sửa lỗi `max(1, int(top_k or 3))` trong `policy/tool.py` khiến `top_k=0` vẫn trả về 3 kết quả.
  4. Sửa lỗi nối dư chuỗi `" - "` ở cuối dòng trong `format/tool.py` khi item không có cả `url` lẫn `source`.

## 4. Bằng chứng

- **File/commit/PR chính trong lịch sử Git:**
  - Commit [`5f916b7`](../../starter_v0/providers/deepseek_provider.py): `feat(provider): add DeepSeek provider support and OpenRouter fallback`
  - Commit [`f3e8f5b`](../../starter_v0/runs/v0_B_base_deepseek_20261110T121637166053.json): `chore(eval): run baseline v0 on deepseek and log metrics`
  - Commit [`a8ad6ed`](../../starter_v0/artifacts/system_prompt.md): `feat(optimize): complete v1, v2, v3 optimization rounds reaching 100% base eval accuracy`
  - Commit [`b97122e`](../../starter_v0/artifacts/version_log.csv): `fix(eval): use deepseek-flash directly across all v0-v3 runs and version_log`
  - Commit [`cdfe1e4`](../../starter_v0/tests/test_tools_todo.py): `feat(tools): add 4 custom tools and complete all unit tests (111 passed, 0 skipped)`
  - Commit [`8816599`](../../starter_v0/data/eval_group.json): `feat(eval): add 10 team eval cases and run group/extension suites (100% pass)`
  - Commit [`1ae2018`](../../starter_v0/app.py): `feat(ui): build Streamlit UI app.py and capture 5-turn live chat transcript`
  - Commit [`e2969a7`](group_report.md) & [`9dc3315`](poster.html): Hoàn thiện báo cáo Phần A & B, poster trực quan và transcript live UI.
- **AI/công cụ đã dùng và cách tự kiểm tra kết quả (theo [RULES.md](../../RULES.md)):**
  - **Công cụ AI đã dùng:** Sử dụng trợ lý lập trình AI (Antigravity / Gemini) để hỗ trợ rà soát log JSON của các lần chạy eval, gợi ý cấu trúc giao diện Streamlit `app.py`, viết khung unit test offline với fixture `fake_http` và kiểm tra đối chiếu các tiêu chí trong `RUBRIC.md`.
  - **Cách tự kiểm tra kết quả:**
    1. **Kiểm tra Unit Tests & Contract:** Chạy trực tiếp `pytest -v` trong `starter_v0/` để xác nhận `test_tool_contract.py` xanh và toàn bộ **111/111 unit tests** pass offline (`0 failed, 0 skipped`).
    2. **Kiểm tra Eval thực tế bằng API thật:** Chạy `run_eval.py` trực tiếp với API thật (`deepseek-flash` + Tavily + Firecrawl + RapidAPI Twitter + arXiv + GitHub + Algolia HN) và kiểm tra từng file JSON trong `starter_v0/runs/` đảm bảo `provider_error_cases == 0` và `measured_cases == total_cases`.
    3. **Kiểm tra Live Chat & Telegram thật:** Tự chạy `chat.py` và giao diện Streamlit `app.py`, kiểm tra tin nhắn được gửi thật lên kênh Telegram sau khi xác nhận ở lượt 5 và đối chiếu với log trong `starter_v0/transcripts/`.

## 5. Tự đánh giá

- **Mức độ hoàn thành:** Hoàn thành **100%** toàn bộ yêu cầu bắt buộc (CP1 -> CP5) và **3/4 hạng mục Bonus** (4 tool mới do nhóm tự viết, gửi Telegram thật sau khi user xác nhận, và Test Challenge `0 skipped` kèm 4 regression tests bắt bug trong tool có sẵn).
- **Bài học rút ra:** Hiểu rõ sự khác biệt giữa việc kiểm thử logic hàm Python bằng **Unit Test** (bắt các lỗi biên như `limit=0`, lỗi nối chuỗi, lỗi mạng) và việc đánh giá hành vi ra quyết định của LLM bằng **Eval Dataset** (phân biệt rõ vai trò của `system_prompt.md` cho chính sách điều phối tổng thể và `tools.yaml` cho ranh giới từng công cụ cũng như quy ước định dạng tham số).
