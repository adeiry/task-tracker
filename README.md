# Task Tracker

A lightweight Task Tracker application built with **FastAPI**, **Pydantic**, and a **vanilla JavaScript Kanban board**. This project was developed as part of an AI-Assisted Coding course to practice REST API development, frontend integration, automated testing, documentation, and AI-assisted software development workflows.

---

## Features

### Core Features

- Create tasks
- View tasks in a Kanban board
- Edit existing tasks
- Delete tasks
- Status transitions (To Do → In Progress → Done)
- Drag-and-drop task movement
- Priority levels (Low, Medium, High)
- Status filtering
- Priority filtering

### Mid-Course Project Features

#### Due Dates

- Optional due dates for tasks
- Edit and remove due dates
- Display due dates on task cards
- Automatic overdue detection
- Overdue highlighting
- Overdue task filtering

#### Tags

- Multiple tags per task
- Create and edit tags
- Automatic tag normalization
- Duplicate tag removal
- Blank tag validation (rejects empty or whitespace-only tags)
- Tag filtering

---

## Extra Improvements

After completing the required mid-course features, additional improvements were made to strengthen the usability and presentation of the application.

### Frontend Task Deletion

- Added a Delete action to the frontend
- Added confirmation before deleting a task
- Connected the frontend action to the existing backend DELETE endpoint
- Added error handling for failed deletion requests
- Verified that deleted tasks are removed from the Kanban board

### Frontend Polish

- Improved task-card styling and spacing
- Added subtle hover and transition effects
- Improved button and form states
- Improved drag-and-drop visual feedback
- Improved tag and due-date presentation
- Improved empty and error states
- Preserved the existing application behavior and API integration

---

## Architecture

The project follows a simple layered architecture designed for learning purposes.

- **FastAPI** – REST API framework
- **Pydantic** – Request and response validation
- **In-memory storage** – Lightweight task storage during application runtime
- **Vanilla JavaScript** – Frontend Kanban board
- **Pytest** – Automated backend testing

The project intentionally excludes:

- Authentication
- Database integration
- Cloud deployment
- Real-time updates

---

## Project Structure

```text
task-tracker/
├── app/
├── frontend/
├── tests/
├── docs/
│   └── midcourse/
│       ├── mini-adr.md
│       ├── prompt-log.md
│       ├── reflection.md
│       ├── user-stories.md
│       └── verification.md
├── README.md
├── requirements.txt
└── ...
```

---

## Prerequisites

- Python 3.10 or later
- pip

---

## Installation

Clone the repository:

```bash
git clone https://github.com/adeiry/task-tracker.git
cd task-tracker
```

Create and activate a virtual environment.

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Backend

Start the FastAPI development server:

```bash
python -m uvicorn app.main:app --reload --port 8000
```

The API will be available at:

```
http://127.0.0.1:8000
```

---

## Running with Docker

Build the image:

```bash
docker build -t task-tracker .
```

Run the container:

```bash
docker run -d --name task-tracker -p 8000:8000 task-tracker
```

The API will be available at the same URL as the local backend:

```
http://127.0.0.1:8000
```

Verify it's running:

```bash
curl http://127.0.0.1:8000/health
```

---

## Running the Frontend

Open the `frontend/index.html` file in a web browser (for example, Google Chrome).

Ensure the backend server is running on port **8000**. The frontend sends requests to the API at:

```text
http://127.0.0.1:8000
```

---

## API Documentation

Once the backend is running, open:

```
http://127.0.0.1:8000/docs
```

Swagger UI provides interactive API documentation for all available endpoints.

---

## Health Check

Verify that the API is running:

```bash
curl http://127.0.0.1:8000/health
```

Example response:

```json
{
  "status": "ok",
  "timestamp": "2026-07-03T12:00:00.000000+00:00"
}
```

---

## Running the Test Suite

Run all backend tests:

```bash
python -m pytest -v
```

---

## AI-Assisted Development Workflow

This project was developed using an AI-assisted workflow.

AI tools were used to:

- Inspect the existing architecture
- Plan feature implementation
- Generate implementation suggestions
- Generate automated tests
- Review completed work
- Verify feature completeness

All AI-generated code and recommendations were reviewed, tested, and validated before being accepted.

The complete AI interaction history is documented in:

- `docs/midcourse/prompt-log.md`

---

## Project Documentation

Additional project documentation is available in the `docs/midcourse/` directory:

- `user-stories.md`
- `mini-adr.md`
- `prompt-log.md`
- `verification.md`
- `reflection.md`

---

## License

This project was created for educational purposes as part of the AI-Assisted Coding course.