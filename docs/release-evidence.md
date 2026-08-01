## Baseline

- Branch: final-project
- Date: 2026-08-01
- Local app run command: `uvicorn app.main:app --reload --port 8000`
- `/health` result: HTTP 200, response: `[paste short actual response]`
- Frontend check: Opened `frontend/index.html` directly in Google Chrome by double-clicking the file in the project folder. The Kanban board loaded with the To Do, In Progress, and Done columns, and the create/edit flow remained visible.
- Test command: `python -m pytest -v`
- Test result: `60 passed in 0.15s`