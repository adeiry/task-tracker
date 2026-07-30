# Task Tracker

A lightweight Task Tracker REST API built with **FastAPI** and **Pydantic**, plus a **vanilla JavaScript Kanban board** frontend. This project was developed as part of an AI-Assisted Coding course (through Module 4) to practice REST API design, containerization, CI, automated testing, and AI-assisted development workflows.

This is a learning project, **not** a production service: there is no authentication, no persistent database (all data lives in memory and resets on restart), and no deployment configuration beyond running the provided Docker image locally.

---

## Project Overview

### Core Features

- Create, view, edit, and delete tasks
- Kanban board with drag-and-drop status changes
- Status transitions (To Do → In Progress → Done)
- Priority levels (Low, Medium, High)
- Status and priority filtering (`GET /tasks?status=`, `GET /tasks?priority=`)

### Due Dates

- Optional due dates for tasks
- Edit and remove due dates
- Automatic overdue detection and highlighting
- Overdue filtering (`GET /tasks?overdue=true|false`)

### Tags

- Multiple tags per task
- Automatic tag normalization (trimmed, case-insensitive de-duplication)
- Blank or whitespace-only tags are rejected (HTTP 422), not silently dropped
- Tag filtering (`GET /tasks?tag=`)

### Extra Improvements

- Frontend delete action (with confirmation) wired to the existing backend `DELETE` endpoint
- Frontend visual polish (card/button/drag-and-drop states, loading/empty/error states)

---

## Prerequisites

- Python 3.11 (this is what CI and the Docker image actually run; the code's `X | None` type hints require at least Python 3.10 to import)
- pip
- Docker, only if you want to run the containerized version (see [Run with Docker](#run-with-docker))

---

## Local Setup

Clone the repository:

```bash
git clone https://github.com/adeiry/task-tracker.git
cd task-tracker
```

Create and activate a virtual environment:

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell)**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Run the App Locally

With the virtual environment active, from the repo root:

```bash
uvicorn app.main:app --reload --port 8000
```

The API is now available at `http://127.0.0.1:8000`.

Verify it's running:

```bash
curl http://127.0.0.1:8000/health
```

Interactive API docs (Swagger UI):

```
http://127.0.0.1:8000/docs
```

### Running the Frontend

Open `frontend/index.html` directly in a browser, with the backend running on port 8000 (the frontend's `BASE_URL` is hardcoded to `http://localhost:8000`).

---

## Run Tests

With the virtual environment active, from the repo root:

```bash
pytest -v
```

`tests/verify_a.py` is a separate, ad hoc manual verification script (prints `PASS`/`FAIL` to stdout) for Pydantic model edge cases — it is not part of the pytest suite and is run directly:

```bash
python tests/verify_a.py
```

---

## Run with Docker

Build the image:

```bash
docker build -t task-tracker .
```

Run the container:

```bash
docker run -d --name task-tracker -p 8000:8000 task-tracker
```

The API is available at the same URL as the local backend:

```
http://127.0.0.1:8000
```

Verify it's running:

```bash
curl http://127.0.0.1:8000/health
```

The image is a multi-stage build (`python:3.11-slim`), installs dependencies from prebuilt wheels, and runs as a non-root `app` user. `CMD` runs `uvicorn app.main:app --host 0.0.0.0 --port 8000` — no `--reload` in the container.

---

## CI Workflow

Defined in `.github/workflows/ci.yml`:

- **Triggers:** every `push` and every `pull_request` (no branch filter configured — this applies to all branches).
- **Job:** a single `test` job on `ubuntu-latest`.
- **Steps:** checkout → set up Python `3.11` → `pip install -r requirements.txt` → `pytest -v`.

You can reproduce the CI job locally with the same [Local Setup](#local-setup) and [Run Tests](#run-tests) commands above. CI does not build or run the Docker image, and there is no configured lint/format step.

---

## Project Structure

```text
task-tracker/
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── main.py            # FastAPI app instance and all route handlers
│   ├── models.py          # Pydantic models: TaskCreate, TaskUpdate, TaskResponse, enums
│   ├── storage.py          # In-memory task store
│   ├── business_rules.py  # Status-transition, overdue, and tag-matching rules
│   ├── api/                # Empty placeholder package
│   ├── repositories/       # Empty placeholder package
│   └── services/           # Empty placeholder package
├── frontend/
│   └── index.html          # Self-contained Kanban board UI (no build step)
├── tests/
│   ├── conftest.py
│   ├── test_tasks.py
│   └── verify_a.py          # Ad hoc manual verification script (not run via pytest)
├── docs/
│   └── midcourse/
│       ├── mini-adr.md
│       ├── prompt-log.md
│       ├── reflection.md
│       ├── user-stories.md
│       └── verification.md
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── CLAUDE.md
└── README.md
```

---

## Project Conventions and Current Limitations

- **No router/service layer.** All route handlers live in `app/main.py` and call directly into `app/storage.py` and `app/business_rules.py`. `app/api/`, `app/repositories/`, and `app/services/` are empty placeholder packages reserved for future structure but currently unused.
- **In-memory storage only.** `app/storage.py` holds tasks in a module-level dict keyed by UUID; all data is lost on restart. There is no database.
- **No authentication.** `CORSMiddleware` is configured with `allow_origins=["*"]` — this is intentionally permissive for local learning use, not appropriate as-is beyond that.
- **Duplicated title validation.** `TaskCreate` and `TaskUpdate` each define a nearly identical `validate_title` field validator in `app/models.py` (unlike tag validation, which was already consolidated into a shared `_normalize_tags` helper).
- **Fixed status-transition set.** Only `ToDo → InProgress`, `InProgress → Done`, and `Done → InProgress` are allowed; a same-status "transition" is explicitly rejected (422), not treated as a no-op.
- **`GET /tasks` result ordering is not a documented contract.** [VERIFY] It currently reflects dict insertion order rather than an explicit sort.
- **`.env.example` declares `PORT` and `APP_ENV`, and `python-dotenv` is a dependency, but nothing in `app/` currently reads either variable.** [VERIFY] The server's host/port are only set via the `uvicorn`/Docker command-line flags shown above.
- **CI runs tests only.** It does not build or verify the Docker image; Docker usage is verified manually.
- **No linter or formatter is configured.**
- Not production-ready: no auth, no database, no deployment configuration — see the overview above.

---

## Documentation and Decisions

There is no dedicated `docs/decisions/` directory. The closest existing technical decision record is:

- [`docs/midcourse/mini-adr.md`](docs/midcourse/mini-adr.md) — architecture decision record for the due-dates and tags features.

Additional project documentation lives in `docs/midcourse/`:

- [`user-stories.md`](docs/midcourse/user-stories.md)
- [`prompt-log.md`](docs/midcourse/prompt-log.md) — the full AI interaction history for this project; all AI-generated code and suggestions were reviewed, tested, and validated before being accepted.
- [`verification.md`](docs/midcourse/verification.md)
- [`reflection.md`](docs/midcourse/reflection.md)

---

## License

This project was created for educational purposes as part of the AI-Assisted Coding course.
