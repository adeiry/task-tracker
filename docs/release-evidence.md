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
- Intentional red run: `https://github.com/adeiry/task-tracker/actions/runs/30716668656`
- Red run result: I temporarily introduced a deliberate test failure and pushed the change. GitHub Actions correctly reported the workflow as failed.
- Recovery evidence: I restored the correct code, pushed the fix, and confirmed that the latest CI run completed successfully.
- Shortcut check: No `continue-on-error`, no `|| true`, pytest is not skipped, dependencies are installed, and the Python version is explicit.

## Docker evidence

- Build command: `docker build -t task-tracker-final .`
- Build result: Successful.
- Run command: `docker run --rm -p 8000:8000 --name task-tracker-final task-tracker-final`
- `/health` check: HTTP 200 from `http://localhost:8000/health`
- Non-root check, if implemented: Implemented. The Dockerfile creates a non-root user (`app`) and runs the application as that user using `USER app`.
- No-baked-secrets check: `.env` is excluded by `.dockerignore`, and no secrets or credentials are copied or declared in the Dockerfile.
- Runtime command: `CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]`

## Documentation claim-vs-reality log

| Claim checked | Evidence used | Result | Change made, if any |
|---|---|---|---|
| README API endpoint list matches the implemented backend routes. | Reviewed `app/main.py` and confirmed the documented `/health` and CRUD task endpoints are implemented. | Pass | No changes needed. |
| README Docker section accurately describes the container configuration. | Compared the README with the `Dockerfile` and `.dockerignore`; verified the multi-stage build, non-root `app` user, exposed port 8000, and exclusion of `.env`. | Pass | No changes needed. |
| README documentation links and project structure reflect the repository contents. | Opened the referenced files under `docs/` and confirmed the documented project folders and files exist. | Pass | No changes needed. |