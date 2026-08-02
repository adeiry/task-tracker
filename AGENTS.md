# AGENTS.md

## Purpose

This repository is a learning-project Task Tracker developed through Module 4 of an AI-Assisted Coding course. Module 5 focuses on grading, review, and governance of AI-assisted work rather than building new application features.

These instructions apply to the entire repository.

## Project Summary

The project contains:

- A FastAPI REST API for creating, retrieving, listing, partially updating, and deleting tasks.
- Pydantic models for request validation and response serialization.
- An in-memory task store; tasks are lost when the process restarts.
- A self-contained vanilla HTML, CSS, and JavaScript Kanban frontend.
- Pytest coverage for API behavior and an additional manual model-verification script.
- A Docker image intended for local use.

This is not a production service. The inspected code has no authentication or persistent database. CORS currently permits every origin.

Primary evidence:

- `README.md`
- `app/main.py`
- `app/models.py`
- `app/storage.py`
- `frontend/index.html`

## Technology Stack

Confirmed from repository files:

- Python 3.11 in CI and Docker.
- FastAPI 0.115.0.
- Uvicorn 0.30.6.
- Pydantic 2.9.2.
- Pytest 8.3.3.
- HTTPX 0.27.2.
- Vanilla HTML, CSS, and JavaScript frontend.
- Docker using a multi-stage `python:3.11-slim` build.
- In-memory Python dictionary storage.

Dependency evidence is in `requirements.txt`. Runtime and container evidence is in `README.md`, `Dockerfile`, and `.github/workflows/ci.yml`.

A database, authentication system, frontend package manager, frontend build tool, linter, formatter, and deployment platform are not confirmed.

## Supported Setup and Commands

Run commands from the repository root.

Create and activate a virtual environment on macOS or Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the API locally:

```bash
uvicorn app.main:app --reload --port 8000
```

Check API health after starting it:

```bash
curl http://127.0.0.1:8000/health
```

Run the pytest suite:

```bash
pytest -v
```

Run the separate manual Pydantic verification script:

```bash
python tests/verify_a.py
```

Build and run the local Docker image:

```bash
docker build -t task-tracker .
docker run -d --name task-tracker -p 8000:8000 task-tracker
```

The frontend has no confirmed build command. With the backend running on port 8000, open `frontend/index.html` directly in a browser. Its JavaScript communicates with the backend at `http://localhost:8000`.

Do not invent commands for linting, formatting, database migration, frontend builds, or deployment. Mark them as `not confirmed` unless supporting configuration is added and inspected.

## Confirmed API Shape

`app/main.py` defines:

- `GET /health`
- `GET /tasks`
- `POST /tasks`
- `GET /tasks/{task_id}`
- `PATCH /tasks/{task_id}`
- `DELETE /tasks/{task_id}`

Task listing can filter by status, priority, overdue state, and tag. When multiple filters are supplied, the storage implementation applies them with AND behavior.

## Confirmed Task Model and Business Rules

### Statuses

The only defined task statuses are:

- `ToDo`
- `InProgress`
- `Done`

The only allowed status transitions are:

- `ToDo` → `InProgress`
- `InProgress` → `Done`
- `Done` → `InProgress`

Same-status updates and other transitions are rejected with HTTP 422 when status-transition validation is reached.

Evidence: `app/models.py`, `app/business_rules.py`, and `app/main.py`.

### Priorities

The only defined priorities are:

- `Low`
- `Medium`
- `High`

New tasks default to `Medium`.

Evidence: `app/models.py`.

### Task Fields and Defaults

A task response contains:

- `id`
- `title`
- `description`
- `status`
- `priority`
- `assignee`
- `due_date`
- `tags`
- `created_at`
- `updated_at`

New tasks default to:

- Status: `ToDo`
- Priority: `Medium`
- Description: empty string
- Assignee: `None`
- Due date: `None`
- Tags: empty list

The storage layer generates a UUID4 string for `id` and UTC timestamps for creation and update times.

Evidence: `app/models.py` and `app/storage.py`.

### Validation

Confirmed validation rules include:

- Titles are trimmed.
- Titles must not be blank.
- Titles must be no longer than 200 characters.
- Unknown fields are rejected on create and update models.
- Tags are trimmed.
- Blank or whitespace-only tags are rejected.
- Tags are deduplicated case-insensitively while preserving the first occurrence's casing.
- Statuses and priorities must match their defined enum values.
- Partial updates apply only explicitly supplied fields.
- An explicitly supplied `null` due date clears the existing due date.

Evidence: `app/models.py`, `app/storage.py`, and `tests/test_tasks.py`.

### Overdue Rule

A task is overdue only when:

- It has a due date.
- The due date is strictly earlier than the current local date supplied by the storage layer.
- Its status is not `Done`.

A task due today is not overdue.

Evidence: `app/business_rules.py`, `app/storage.py`, and `tests/test_tasks.py`.

### Tag Matching

Tag filtering:

- Ignores leading and trailing whitespace.
- Is case-insensitive.
- Requires an exact normalized match.
- Does not use substring matching.

Evidence: `app/models.py`, `app/business_rules.py`, and `tests/test_tasks.py`.

## Storage and Architecture

`app/storage.py` stores tasks in a module-level dictionary keyed by task ID. There is no confirmed database or durable persistence. Stored tasks reset when the process restarts.

Route handlers currently live directly in `app/main.py` and call `app/storage.py` and `app/business_rules.py`. The `app/api/`, `app/repositories/`, and `app/services/` packages are currently placeholders.

Do not describe placeholder packages as implemented architecture.

## Module 5 Guardrails

For Module 5 work:

- Prefer read-only repository inspection first.
- Treat grading, review, documentation, and governance as the default scope.
- Use a docs-first approach for proposed changes.
- Work on one bounded task per Codex thread.
- Final-course deliverable work must remain on the `final-project` branch.
- Before recording final evidence, confirm the current branch rather than assuming it.
- Do not add features unless the user explicitly changes the scope.
- Do not modify files under `app/` unless the user explicitly approves one specific minimal fix.
- By default, make documentation changes only under `docs/`.
- `AGENTS.md` may be created or updated when the user explicitly requests repository-agent guidance.
- Do not edit tests, frontend code, dependency files, CI configuration, or container configuration without explicit approval.
- Any approved change under `app/` or `frontend/` must be documented in `docs/final-ai-review.md`, including the reason, files changed, verification performed, and whether the change was suggested by AI.
- Before editing, state the intended task, files to inspect or change, and whether permission is required.
- Show proposed governance or documentation content before applying it when the user asks for prior review.
- Do not run tests or start the app unless the current task authorizes it.
- Keep changes narrowly scoped and preserve unrelated user work.
- Do not accept or submit a changed line, command, configuration choice, or AI recommendation unless the user can explain why it belongs in the repository.

## Evidence and Reporting Rules

When analyzing or reviewing this repository:

- Cite the actual files inspected.
- Use exact paths and line references when useful.
- Distinguish source-code evidence from README claims.
- Prefer executable code and configuration as evidence when documentation conflicts with implementation.
- Say `not confirmed` when a command, behavior, configuration, or requirement is not visible.
- Do not infer behavior from filenames alone.
- Do not invent findings, test outcomes, repository history, runtime behavior, or architectural intent.
- Do not claim that tests pass unless they were authorized and actually run.
- Clearly label assumptions and items requiring verification.
- Note stale or contradictory comments rather than silently treating them as current behavior.

## Security and Governance

- Never paste, expose, log, or commit secrets, credentials, API keys, tokens, private keys, or sensitive environment values.
- Never paste, expose, log, or commit real personal data, customer data, production logs, `.env` contents, or confidential business information.
- Do not open or reproduce secret-bearing files unless the task explicitly requires a safe inspection.
- Do not run destructive commands such as recursive deletion, hard resets, forced checkouts, or destructive database operations.
- Do not overwrite or discard unrelated user changes.
- Do not install packages, access external services, publish artifacts, push branches, or create pull requests without explicit authorization.
- Use read-only commands for discovery and verification whenever possible.
- Treat the permissive CORS setting and lack of authentication as learning-project limitations, not production-ready security.
- If evidence is missing, inaccessible, ambiguous, or contradictory, report that limitation instead of guessing.

## Verification Expectations

Choose verification proportional to the approved task:

- Documentation-only work: inspect the rendered text or diff; tests are normally unnecessary unless requested.
- Python behavior changes: run the smallest relevant test selection first, then consider `pytest -v` if authorized.
- Frontend changes: inspect `frontend/index.html` and perform browser verification only if authorized.
- Docker changes: Docker build or run verification requires explicit task scope and may require user approval.
- When reviewing CI, flag `continue-on-error`, `|| true`, skipped or conditional pytest execution, unpinned or vague Python versions, and missing dependency-installation steps.
- Do not describe a workflow as successful only because the job is green; confirm that pytest actually ran.

Always report exactly what was and was not verified.
