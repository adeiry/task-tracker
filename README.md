# Task Tracker API

A minimal learning-project REST API built with **FastAPI** and **Pydantic**, using JSON file-based storage for persistence (see ADR-001). This project is intended for learning backend fundamentals — REST API design, request validation, and application structure — not for production use.

## Architecture

- **FastAPI** — REST API framework
- **Pydantic** — request/response validation
- **Service layer** — business logic
- **Repository layer** — JSON file persistence (`data/tasks.json`)
- No database, authentication, Docker, or cloud deployment (see ADR-001 for rationale)

## Prerequisites

- Python 3.10+
- pip

## Setup

1. Clone or download this project and navigate into it:
```bash
   cd task-tracker
```

2. Create and activate a virtual environment:

   **Linux/macOS:**
```bash
   python3 -m venv venv
   source venv/bin/activate
```

   **Windows (PowerShell):**
```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
```

3. Install dependencies:
```bash
   pip install -r requirements.txt
```

4. Copy the example environment file:

   **Linux/macOS:**
```bash
   cp .env.example .env
```

   **Windows (PowerShell):**
```powershell
   Copy-Item .env.example .env
```

## Running the Server

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://127.0.0.1:8000`.

## Testing the Health Endpoint

```bash
curl http://127.0.0.1:8000/health
```

Expected response shape:

```json
{
  "status": "ok",
  "timestamp": "2026-07-03T12:00:00.000000+00:00"
}
```

## API Documentation (Swagger UI)

Once the server is running, open your browser to: