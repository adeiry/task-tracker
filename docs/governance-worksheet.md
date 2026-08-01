# Governance Retrospective - AI-Assisted Coding

## What I Shared With AI

| Item | Module | Risk Level | Reason |
|------|--------|------------|--------|
| Task Tracker source code | 2–5 | Low | It was source code from a course learning project and did not contain known secrets, personal data, customer information, or proprietary production logic. |
| Test output and stack traces | 2–4 | Medium | Test output and stack traces may reveal local paths, usernames, request data, environment details, or internal implementation information, even when the project itself is non-sensitive. |
| Frontend code (HTML, CSS, JavaScript) | 3 | Low | It was frontend code for a local course project and did not contain known credentials, personal data, private service addresses, or proprietary business information. |
| Dockerfile and GitHub Actions CI workflow (YAML) | 4 | Low | They contained standard course-project build and test configuration, with no known embedded secret values, private infrastructure details, or production deployment information. |
| Real external data | Not applicable | Not applicable | I did not knowingly share real customer, personal, production, regulated, or confidential external data with AI during this project. |

## What I Received From AI

| Generated Thing | Module | Do I Understand It Line by Line? | Action |
|----------------|--------|-----------------------------------|--------|
| Backend modules and validators | 2 | Partially | I inspected the generated code, corrected assumptions, and verified its behavior using the model verification script, CRUD checks, pytest, and deliberate break tests. I will review any remaining unclear helper logic before claiming full ownership. |
| Frontend Kanban board and drag-and-drop logic | 3 | Partially | I inspected the code and verified the main behavior in the browser and DevTools, including task rendering, PATCH requests, and failed-move rollback. I marked any event-handling logic I could not explain for further review. |
| GitHub Actions CI workflow | 4 | Yes | I reviewed each workflow step, confirmed when it runs, checked the Python setup and test commands, and verified that the workflow passed in GitHub Actions. |
| Dockerfile | 4 | Yes | I reviewed every instruction, built the image, ran the container, and verified the application health endpoint. I also checked that the container runs as a non-root user and does not copy secrets. |
| Security findings and governance recommendations | 5 | Yes | I reviewed each finding, separated real project risks from course-scope or deployment-context limitations, graded the findings myself, and rewrote the final governance rules in concrete language I can follow. |
