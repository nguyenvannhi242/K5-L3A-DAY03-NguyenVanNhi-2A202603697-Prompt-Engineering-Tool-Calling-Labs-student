---
name: save_report
track: bonus
kind: action
provider: local_filesystem
requires_env: []
inputs: [title, content, filename, confirmed]
outputs: [status, path, bytes_written]
side_effect: local_file_write
requires_confirmation: true
---
# save_report

Saves a markdown research report or digest to `starter_v0/saved_reports/<filename>.md`.
Requires explicit user confirmation (`confirmed=true`) before writing to disk.
