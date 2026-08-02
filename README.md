# Task Tracker

A lightweight Task Tracker REST API built with **FastAPI** and **Pydantic**, plus a self-contained **vanilla HTML, CSS, and JavaScript Kanban board**. The project was developed through all five modules of an AI-Assisted Coding course to practice API design, validation, testing, frontend integration, containerization, continuous integration, security review, and responsible AI-assisted development.

This is a learning project, not a production service. It has no authentication or persistent database: tasks are stored in memory and are lost whenever the backend process restarts. CORS is intentionally permissive for local use.

---

## Project Overview

The application provides a FastAPI REST API and a browser-based Kanban interface for managing tasks. The backend uses Python 3.11, FastAPI, Pydantic, and an in-memory store; pytest and HTTPX support automated API testing. The repository also includes a multi-stage Dockerfile for building a container image and a GitHub Actions test workflow.

### Features

- Create, list, retrieve, partially update, and delete tasks
- Kanban board with create/edit/delete flows and drag-and-drop status changes
- Controlled status workflow: `ToDo` → `InProgress` → `Done`, with `Done` → `InProgress` also supported
- Priority levels: `Low`, `Medium`, and `High`
- Optional descriptions, assignees, due dates, and tags
- Overdue detection and frontend highlighting; tasks due today or marked `Done` are not overdue
- Filtering by status, priority, overdue state, and exact case-insensitive tag match; combined API filters use AND behavior
- Pydantic validation for titles, enum values, dates, tags, and unknown fields
- Case-insensitive tag de-duplication while preserving the first occurrence's casing
- Health-check endpoint
- Frontend loading, empty, error, confirmation, and failed-drag rollback states

---

## Prerequisites

- Python 3.11 (used by CI and Docker; the code requires at least Python 3.10)
- `pip`
- Docker, only for containerized use

---

## Project Structure

```text
task-tracker/
├── .github/workflows/ci.yml  # GitHub Actions test workflow
├── app/
│   ├── main.py               # FastAPI application and route handlers
│   ├── models.py             # Pydantic models, enums, defaults, and validation
│   ├── storage.py            # In-memory task storage and filtering
│   └── business_rules.py     # Workflow, overdue, and tag-matching rules
├── frontend/index.html       # Self-contained Kanban UI; no build step
├── tests/                    # Pytest API tests and manual model verification
├── docs/                     # Architecture, verification, AI, security, and governance records
├── Dockerfile
├── .dockerignore
├── requirements.txt
└── README.md
```

The `app/api/`, `app/repositories/`, and `app/services/` packages are currently empty placeholders; they are not implemented application layers.

---

## API

With the backend running, Swagger UI is available at:

```text
http://127.0.0.1:8000/docs
```

The implemented endpoints are:

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Return service liveness and a UTC timestamp |
| `GET` | `/tasks` | List tasks, optionally filtering by `status`, `priority`, `overdue`, and `tag` |
| `POST` | `/tasks` | Create a task |
| `GET` | `/tasks/{task_id}` | Retrieve one task |
| `PATCH` | `/tasks/{task_id}` | Partially update a task |
| `DELETE` | `/tasks/{task_id}` | Delete a task |

---

## Running Locally

Clone the repository and enter it:

```bash
git clone https://github.com/adeiry/task-tracker.git
cd task-tracker
```

Create and activate a virtual environment.

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

Run the API from the repository root:

```bash
uvicorn app.main:app --reload --port 8000
```

Open Swagger UI at `http://127.0.0.1:8000/docs`, or check service health with:

```bash
curl http://127.0.0.1:8000/health
```

### Running the Frontend

With the backend running on port 8000, open `frontend/index.html` directly in a browser. The frontend has no package manager or build command and communicates with `http://localhost:8000`.

---

## Running Tests

With the virtual environment active, run the pytest suite from the repository root:

```bash
pytest -v
```

`tests/verify_a.py` is a separate manual Pydantic model-verification script and is not part of the pytest suite:

```bash
python tests/verify_a.py
```

---

## Docker

Build the image:

```bash
docker build -t task-tracker .
```

Run the container:

```bash
docker run -d --name task-tracker -p 8000:8000 task-tracker
```

The container exposes port `8000` and runs Uvicorn without development reload mode. The multi-stage `python:3.11-slim` image installs dependencies from locally built wheels and runs the application as the non-root `app` user.

Secrets are not baked into the image: the Dockerfile copies only `requirements.txt` and `app/`, while `.dockerignore` excludes `.env` files except the placeholder `.env.example`. No credentials or secret values are declared in the Dockerfile.

---

## Continuous Integration

The GitHub Actions workflow in `.github/workflows/ci.yml` runs automatically on every push and pull request. It checks out the repository, configures Python 3.11, installs the pinned direct dependencies from `requirements.txt`, and runs `pytest -v` on `ubuntu-latest`.

CI currently tests the Python application only; it does not run linting, formatting, or a Docker build.

---

## Documentation

Important project records include:

- [`docs/architecture.md`](docs/architecture.md) — final architecture overview and context-engineering reflection
- [`docs/midcourse/mini-adr.md`](docs/midcourse/mini-adr.md) — architecture decision record for due dates and tags
- [`docs/midcourse/user-stories.md`](docs/midcourse/user-stories.md) — feature requirements and corrected AI assumptions
- [`docs/midcourse/verification.md`](docs/midcourse/verification.md) — backend and browser verification report
- [`docs/midcourse/prompt-log.md`](docs/midcourse/prompt-log.md) — detailed AI prompt, decision, and verification history
- [`docs/midcourse/reflection.md`](docs/midcourse/reflection.md) — development reflection and lessons learned
- [`docs/ai-usage.md`](docs/ai-usage.md) and [`docs/ai-playbook.md`](docs/ai-playbook.md) — AI usage rules and review practices
- [`docs/security-review.md`](docs/security-review.md) — AI-assisted findings, manual review, reconciliation, and security backlog
- [`docs/governance-worksheet.md`](docs/governance-worksheet.md) — retrospective on information shared with AI and generated work accepted
- [`docs/release-evidence.md`](docs/release-evidence.md) — recorded local, CI, and Docker release checks
- [`docs/decisions/comments-feature-plan.md`](docs/decisions/comments-feature-plan.md) — a design proposal only; comments are not implemented

---

## AI-Assisted Development

AI was used as a development assistant across planning, implementation, testing, documentation, review, and governance. Generated code and recommendations were inspected, refined, and accepted only after appropriate tests or manual verification. Prompts, decisions, corrections, and verification evidence are recorded in the project documentation for transparency and traceability.

---

## Security

Implemented practices include:

- Pydantic request validation, enum constraints, title limits, tag normalization, and rejection of unknown fields
- Escaping of task content before the frontend inserts it into HTML
- Exact versions for direct Python dependencies in `requirements.txt`
- `.env` exclusion from Git and Docker build context; the Dockerfile contains no secret values
- Multi-stage Docker build with a non-root runtime user and no Uvicorn reload mode
- AI-assisted and manual security review with findings graded and prioritized in `docs/security-review.md`

Current limitations remain important: there is no authentication or authorization, CORS allows all origins, several input fields and collection sizes are unbounded, storage is unbounded and in-memory, and no dependency or container scanning is configured. Keep the service local or on a trusted network unless these issues are addressed.

---

## Current Limitations

- Tasks are stored in a module-level dictionary and disappear on restart.
- There is no authentication, authorization, database, pagination, or production deployment configuration.
- Route handlers live directly in `app/main.py`; the placeholder API, repository, and service packages are unused.
- The frontend API URL is fixed to `http://localhost:8000`.
- Task ordering reflects current dictionary insertion order rather than an explicit API sorting contract.
- `.env.example` defines `PORT` and `APP_ENV`, but the application does not currently read them.
- No linter, formatter, or frontend build tool is configured.

---

## Future Improvements

- Add persistent database storage and migrations.
- Add authentication and per-user authorization before shared deployment.
- Add pagination, capacity controls, and bounds for descriptions, assignees, and tags.
- Restrict CORS and make the frontend API URL environment-specific.
- Introduce clearer router, service, and repository layers if the application grows.
- Add linting, dependency scanning, container scanning, and Docker verification to CI.
- Implement task comments after reviewing the existing design proposal.

---

## License

This project was created for educational purposes as part of the AI-Assisted Coding course.
