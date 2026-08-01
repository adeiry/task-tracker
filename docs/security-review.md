# Security Review

This document records AI-generated security findings for student review. A finding may describe a production risk even when the underlying behavior is an intentional course-scope decision. The **Grade** and **Reason** columns are intentionally blank for the student to complete.

Course-scope or deployment-context findings include:

- SEC-01: authentication and authorization are intentionally absent from this local learning project.
- SEC-03: in-memory storage and the lack of pagination are part of the minimal course architecture.
- SEC-04: permissive CORS is explicitly documented as suitable only for local learning use.
- SEC-06: stronger supply-chain controls are hardening measures for broader use.
- SEC-07: explicit CI token permissions are defense-in-depth and also depend on repository settings.

| Severity | File/line | Finding | Suggested fix | Grade | Reason |
|---|---|---|---|---|---|
| High if network-exposed; accepted limitation for local coursework | `app/main.py:52`; `README.md:5` | **SEC-01:** All task operations lack authentication and authorization. Any client that can reach the API can list, read, create, modify, or delete every task. | Keep the service bound to trusted/local environments. Before any shared deployment, define authentication and per-task authorization requirements and add tests for anonymous and cross-user access. | Valid | I agree with this finding because the API does not implement authentication or authorization, so anyone with access to the API can perform all task operations. However, this was an intentional decision for the course project since authentication is outside the project scope. I consider it a valid security concern for a production application, but an accepted limitation for this assignment. |
| Medium | `app/models.py:51`; `app/models.py:108` | **SEC-02:** Several user-controlled fields and collections are unbounded. `description` and `assignee` have no length limits, and individual tags and the number of tags are unrestricted. | Establish course-appropriate bounds for descriptions, assignees, tag length, and tag count. For deployment, also enforce an HTTP request-body limit at the server or proxy. | Valid | I consider this finding valid because several user-controlled fields, such as the description, assignee, and tags, do not have size limits. Although this is unlikely to cause problems in a small local project, adding reasonable limits would make the application more robust and reduce the risk of excessive resource usage. |
| Medium | `app/storage.py:8`; `app/storage.py:68`; `app/main.py:52` | **SEC-03:** Task creation and listing have no capacity or pagination controls, enabling memory and response-amplification exhaustion. Every task remains in a module-level dictionary until deletion or restart, and `GET /tasks` returns the complete collection. | For local coursework, document the capacity limitation. Before broader use, add pagination or result limits, request throttling, and bounded or persistent storage. | Valid | I agree with this finding because tasks are stored in memory without any capacity limit, and the API always returns the full list of tasks. This could become a resource issue if the application stored a large amount of data. Since this project is designed as a small learning application, I see it as an accepted design limitation rather than something that needs to be fixed. |
| Medium if network-exposed; accepted limitation for local coursework | `app/main.py:24`; `frontend/index.html:725` | **SEC-04:** CORS permits every origin, method, and header while also enabling credentials. The frontend assumes a local API at `http://localhost:8000`. | For local-only use, consider disabling credentials because the app has no credential mechanism. For any hosted environment, use an explicit origin allowlist and an environment-specific frontend API URL. | Valid | I agree that the CORS configuration is very permissive. For this project it is acceptable because the application is only intended to run locally and does not use authentication or cookies. However, the same configuration would not be appropriate for a production deployment, so I consider it a valid finding. |
| Low | `app/main.py:130`; `app/main.py:176`; `app/main.py:243` | **SEC-05:** Path IDs are unbounded strings and are reflected into 404 response details. This can produce oversized responses and unnecessary reflection, although JSON encoding prevents direct HTML injection in the API response. | Parse IDs as UUIDs or apply a strict length and pattern constraint. Return a fixed message such as `Task not found` rather than reflecting client-controlled input. | Noise | Although the API reflects the provided task ID in 404 responses, I do not think this creates a meaningful security issue in this project. The value is returned as JSON, no sensitive information is exposed, and no realistic attack scenario is demonstrated. I see this more as a small API design improvement than a security finding. |
| Low | `requirements.txt:1`; `.github/workflows/ci.yml:12`; `Dockerfile:4` | **SEC-06:** Supply-chain controls are basic. Direct dependencies are version-pinned, but transitive dependencies are not hash-locked, CI actions and the Docker base use mutable tags, and no dependency or image scan is configured. | Pin CI actions to commit SHAs, pin the container base by digest, adopt a hash-backed lock process, and add dependency or image scanning if the project's governance scope expands. | Valid | I agree that the project could be improved by using stronger supply-chain security practices, such as pinning dependencies and CI actions more strictly. These are good production practices, but they are outside the goals of this learning project. I consider the finding valid, although I would not treat it as something that must be implemented for this assignment. |
| Low | `.github/workflows/ci.yml:7` | **SEC-07:** CI does not declare least-privilege token permissions, so effective access depends on repository settings and GitHub defaults. | Add an explicit minimal declaration, normally `permissions: contents: read`, unless future workflow steps require more access. | Noise | I understand the recommendation to explicitly define GitHub Actions permissions, but I do not think there is enough evidence that the current workflow introduces a real security risk. The workflow only checks out the code, installs dependencies, and runs tests, so this feels more like a general best practice than a meaningful security issue for this project. |

## Manual Security Review

After reviewing the AI findings, I performed a manual security review of the project to verify whether additional security issues were present.

### Manual checks performed

| Check | Result | Notes |
|---|---|---|
| Frontend output encoding | Pass | Verified that task title, description, assignee, tags, and due date are escaped using `escapeHtml()` before being rendered with `innerHTML`. No stored XSS issue identified. |
| HTML injection test | Pass | Created a task containing HTML-like input and confirmed that the frontend displays the content safely as text instead of interpreting it as HTML. |
| Tag rendering | Pass | Confirmed that tags are escaped before being inserted into the DOM. |
| Internal exception handling | Pass | Searched the backend for broad exception handling and raw exception messages returned to clients. No evidence of internal exception information being exposed. |
| Docker runtime configuration | Pass | Verified that the Docker container runs Uvicorn without `--reload` and uses a non-root user. |

### Manual review summary

I manually reviewed the frontend rendering, backend error handling, and deployment configuration to look for additional security issues beyond those identified by the AI. I specifically tested HTML-like input to check for stored XSS and inspected how user-controlled values are rendered in the frontend. Because all displayed values are escaped before being inserted into the page, I did not identify any additional confirmed security vulnerabilities. The manual review supports the AI findings but did not reveal any new issues requiring further action.

## Finding Reconciliation

| Agreement | AI-only | You-only |
|---|---|---|
| None independently identified. The manual scan verified clean areas rather than reporting issues overlapping the AI findings. | SEC-01: missing authentication and authorization; SEC-02: unbounded input fields and tags; SEC-03: unbounded in-memory storage and full-list responses; SEC-04: permissive CORS; SEC-05: reflected, unconstrained task IDs; SEC-06: basic supply-chain controls; SEC-07: no explicit CI token permissions. | None. The manual scan found no additional confirmed security issues. |

The passing checks for output encoding, HTML injection, tag rendering, exception handling, and Docker runtime configuration are useful negative findings. They are not placed under Agreement because the AI did not report vulnerabilities in those areas.

## Observation About AI Coverage

AI coverage was broad across backend validation, access control, resource exhaustion, CORS, dependencies, containers, and CI, but it produced two low-value findings that I graded as Noise.  
My manual review added depth around frontend XSS safety and error handling, confirming clean areas, but it did not uncover a You-only vulnerability.

## Top-3 Security Backlog

| Rank | Finding | Why it matters | Suggested owner | Next action |
|---|---|---|---|---|
| 1 | SEC-01 — No authentication or authorization | Any client that reaches the API can read and modify all tasks. It is accepted for this assignment but is the clearest blocker to using the application in a shared or production environment. | Course/project owner, then backend | Document that deployment must remain local or trusted. If the project scope expands, define authentication and task-authorization requirements before implementation. |
| 2 | SEC-02 — Unbounded user-controlled fields and tags | Very large descriptions, assignees, tags, or tag lists can increase memory and processing use. This is a concrete robustness gap even though the local-project risk is limited. | Backend | Propose and document reasonable maximum lengths and tag-count limits for create and update models, then add boundary tests if a fix is approved. |
| 3 | SEC-03 — Unbounded task storage and full-list responses | Memory consumption and response size grow with every task. Large collections could degrade or exhaust the service. | Backend and course/project owner | Document the current capacity limitation. If broader use is planned, define pagination, result limits, and an appropriate storage strategy. |
