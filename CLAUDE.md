# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

A minimal learning-project REST API built with FastAPI and Pydantic. Intended for learning backend fundamentals (REST API design, request validation, application structure) — not for production use. No database, authentication, Docker, or cloud deployment.

## Commands

Activate the virtual environment first: `source venv/bin/activate`

- Run the server: `uvicorn app.main:app --reload --port 8000`
- Run all tests: `pytest`
- Run a single test file: `pytest tests/test_tasks.py`
- Run a single test: `pytest tests/test_tasks.py::test_rejects_patch_when_updating_task_to_same_status`
- Health check once running: `curl http://127.0.0.1:8000/health`
- Interactive API docs: `http://127.0.0.1:8000/docs` (Swagger UI) once the server is running

There is no configured lint/format command in this repo.

## Architecture

- `app/main.py` — FastAPI app instance and all route handlers (`/health`, `/tasks` CRUD). Routes call directly into `storage` and `business_rules`; there is no separate router/controller layer.
- `app/models.py` — Pydantic models: `TaskCreate`, `TaskUpdate`, `TaskResponse`, and the `TaskStatus`/`TaskPriority` enums. All models use `extra="forbid"`, so unknown fields are rejected. `title` validation (non-blank, ≤200 chars) is duplicated across `TaskCreate` and `TaskUpdate` via separate `field_validator`s.
- `app/storage.py` — in-memory task store (`_tasks: dict[str, TaskResponse]`), keyed by UUID. Despite the README describing a repository layer with JSON file persistence (`data/tasks.json`), the current implementation holds everything in a module-level dict that resets on restart. `_reset()` clears state and is used by test fixtures.
- `app/business_rules.py` — status transition validation. `VALID_TRANSITIONS` is a `frozenset` of allowed `(from, to)` pairs: ToDo→InProgress, InProgress→Done, Done→InProgress. Same-status "transitions" are explicitly rejected (422), not treated as no-ops. `validate_status_transition` raises `HTTPException` directly (422) rather than returning a bool.
- `app/api/`, `app/repositories/`, `app/services/` — currently empty placeholder packages (only `__init__.py`); logic that would conventionally live there is presently all in `main.py`/`storage.py`/`business_rules.py`.
- `frontend/index.html` — single self-contained HTML/JS file (no build step) implementing a Kanban board UI against the API. Talks to the backend via `BASE_URL = 'http://localhost:8000'` hardcoded near the top of the `<script>` block. Open directly in a browser (with the API server running) to use it.

## Key behaviors to know before changing code

- `PATCH /tasks/{id}` has two code paths in `main.py`: when `payload.status` is `None` it updates directly via `storage.update_task`; when a status is present it first fetches the existing task, runs `validate_status_transition`, then updates. Keep both paths consistent if you touch update logic.
- `storage.update_task` uses `payload.model_dump(exclude_unset=True)` so PATCH only overwrites fields explicitly sent by the client.
- Tests reset shared state via `storage._tasks.clear()` in the `client` fixture (`tests/test_tasks.py`) — new tests needing a clean slate should follow this pattern rather than assuming isolation between tests.
- `tests/verify_a.py` is an ad hoc manual verification script (prints PASS/FAIL, not a pytest suite) for Pydantic model validation edge cases — run directly with `python tests/verify_a.py`, not via `pytest`.
