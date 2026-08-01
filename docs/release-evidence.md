## Baseline

- Branch: final-project
- Date: 2026-08-01
- Local app run command: `uvicorn app.main:app --reload --port 8000`
- `/health` result: HTTP 200, response: `[paste short actual response]`
- Frontend check: Opened `frontend/index.html` directly in Google Chrome by double-clicking the file in the project folder. The Kanban board loaded with the To Do, In Progress, and Done columns, and the create/edit flow remained visible.
- Test command: `python -m pytest -v`
- Test result: `60 passed in 0.15s`

## CI evidence

- Workflow file: `.github/workflows/ci.yml`
- Latest run link or note: `https://github.com/adeiry/task-tracker/actions/runs/30716740285`
- Test command used by CI: `pytest -v`
- Shortcut check: No `continue-on-error`, no `|| true`, pytest is not skipped, dependencies are installed, and the Python version is explicit.

## Docker evidence

- Build command: `docker build -t task-tracker-final .`
- Build result: Successful.
- Run command: `docker run --rm -p 8000:8000 --name task-tracker-final task-tracker-final`
- `/health` check: HTTP 200 from `http://localhost:8000/health`
- Non-root check, if implemented: Implemented. The Dockerfile creates a non-root user (`app`) and runs the application as that user using `USER app`.
- No-baked-secrets check: `.env` is excluded by `.dockerignore`, and no secrets or credentials are copied or declared in the Dockerfile.
- Runtime command: `CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]`