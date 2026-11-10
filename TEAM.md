# Team

## Thông tin nhóm

- Tên nhóm: **K5-L3A-DAY03 — Nguyễn Văn Nhi (`2A202603697`)** (Làm cá nhân)
- Lớp: **L3A**
- Repo nhóm: `K5-L3A-DAY03-NguyenVanNhi-2A202603697-Prompt-Engineering-Tool-Calling-Labs-student` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt:
  - **URL repo:** `https://github.com/nguyenvannhi242/K5-L3A-DAY03-NguyenVanNhi-2A202603697-Prompt-Engineering-Tool-Calling-Labs-student`
  - **Nhánh nộp:** `main`
  - **Các commit kỹ thuật chính:** `5f916b7`, `f3e8f5b`, `a8ad6ed`, `b97122e`, `cdfe1e4`, `8816599`, `1ae2018`, `e2969a7`, `9dc3315`, `9122e64` (và commit hoàn thiện cấu trúc báo cáo mới trên `HEAD` nhánh `main`)

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Nguyễn Văn Nhi | `2A202603697` | `nguyenvannhi224@gmail.com` | `nguyenvannhi242` (`hagasei`) | Team Lead / Full-stack AI Engineer (Thực hiện cá nhân 100%) |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Báo cáo cá nhân của thành viên: [`report/team/2A202603697_NguyenVanNhi.md`](report/team/2A202603697_NguyenVanNhi.md).

## NguyenVanNhi-2A202603697

### Phần việc phụ trách

- Thực hiện toàn bộ 5 Checkpoints (CP1–CP5) và 3 hạng mục Bonus:
  - **CP1:** Thiết lập môi trường, cấu hình API keys, tích hợp `deepseek-flash` & `openrouter`, chạy baseline `v0` (`20/20 measured_cases`, `0 provider_error_cases`) và phân tích 9 case FAIL.
  - **CP2:** Tối ưu `artifacts/system_prompt.md` và `artifacts/tools.yaml` qua 3 vòng `v1`, `v2`, `v3` (mỗi vòng 1 giả thuyết rõ ràng), nâng `case_accuracy` từ `0.55` lên **`1.00` (20/20)**.
  - **CP3 (Bonus >3 tools + Test Challenge):** Xây dựng 4 tool mới (`github_search`, `hn_search`, `source_credibility`, `save_report`), sửa 4 bug biên trong các tool có sẵn (`timeline`, `social_search`, `policy`, `format`), và hoàn thiện toàn bộ unit test suite (**111 passed, 0 failed, 0 skipped**).
  - **CP4:** Thiết kế 10 case eval nhóm trong `starter_v0/data/eval_group.json` (5 single-turn `G01`–`G05` + 5 multi-turn `G06`–`G10`) và chạy đánh giá đạt **10/10 PASS (`100%`)** (cùng bộ extension 10/10 PASS).
  - **CP5 (kèm Bonus gửi Telegram thật):** Xây dựng giao diện Streamlit `starter_v0/app.py`, mở public link qua Cloudflare Tunnel, tạo poster `report/team/poster.html`, chạy live chat xác nhận & gửi tin nhắn thật lên Telegram (`status="sent"`), và viết đầy đủ báo cáo `report/team/group_report.md` + `report/team/2A202603697_NguyenVanNhi.md`.

### Đóng góp cụ thể

- Tối ưu `starter_v0/artifacts/system_prompt.md` và `starter_v0/artifacts/tools.yaml`, ghi log đầy đủ vào `starter_v0/artifacts/version_log.csv`.
- Viết mới 4 công cụ trong `starter_v0/tools/` (`github_search`, `hn_search`, `source_credibility`, `save_report`) kèm `TOOL.md` và 12 unit tests.
- Hoàn thiện 13 test stubs + 4 regression tests trong `starter_v0/tests/test_tools_todo.py` (tổng 29 tests trong file, 111 tests toàn suite).
- Xây dựng giao diện `starter_v0/app.py`, `report/team/poster.html` và hoàn thiện bộ báo cáo chuẩn mới trong `report/team/`.

### Bằng chứng

- **Eval Runs (`starter_v0/runs/`):**
  - Baseline `v0`: [`v0_B_base_deepseek_20261110T121637166053.json`](starter_v0/runs/v0_B_base_deepseek_20261110T121637166053.json)
  - Vòng `v1`: [`v1_B_base_deepseek_20261110T121739935133.json`](starter_v0/runs/v1_B_base_deepseek_20261110T121739935133.json)
  - Vòng `v2`: [`v2_B_base_deepseek_20261110T121846914500.json`](starter_v0/runs/v2_B_base_deepseek_20261110T121846914500.json)
  - Vòng `v3` (Base 20/20): [`v3_B_base_deepseek_20261110T121412291861.json`](starter_v0/runs/v3_B_base_deepseek_20261110T121412291861.json)
  - Vòng `v3` (Group 10/10): [`v3_B_group_deepseek_20261110T122202917812.json`](starter_v0/runs/v3_B_group_deepseek_20261110T122202917812.json)
  - Vòng `v3` (Extension 10/10): [`v3_B_extension_deepseek_20261110T122321694058.json`](starter_v0/runs/v3_B_extension_deepseek_20261110T122321694058.json)
- **Live Chat Transcripts (`starter_v0/transcripts/`):**
  - [`v3_deepseek_20261110T122446251190.transcript.json`](starter_v0/transcripts/v3_deepseek_20261110T122446251190.transcript.json) (5 lượt, có xác nhận và gửi Telegram thật ở Turn 4–5)
  - [`v3_ui_deepseek_20261110T141722493242.transcript.json`](starter_v0/transcripts/v3_ui_deepseek_20261110T141722493242.transcript.json)
- **Báo cáo & Unit Tests:**
  - Báo cáo nhóm: [`report/team/group_report.md`](report/team/group_report.md)
  - Báo cáo cá nhân: [`report/team/2A202603697_NguyenVanNhi.md`](report/team/2A202603697_NguyenVanNhi.md)
  - Unit tests: [`starter_v0/tests/test_tools_todo.py`](starter_v0/tests/test_tools_todo.py) (`pytest`: `111 passed, 0 failed, 0 skipped`)
