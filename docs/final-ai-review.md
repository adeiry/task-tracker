# Final AI Review and Ownership Evidence

## AGENTS.md guardrails

- Repo-specific stack and commands included: Yes
- Docs-first/read-first guardrail included: Yes
- Unexpected app/frontend edits rule included: Yes

## AI code review mini-log

**Reviewed file:** `.github/workflows/ci.yml`

| AI comment | Grade: Useful / Noise / Wrong | Reason | Verification or decision |
|---|---|---|---|
| The workflow steps are not indented beneath `steps:`. | **Wrong** | The formatting shown to Codex did not match the actual repository file. The real workflow uses valid YAML indentation. | Inspected `.github/workflows/ci.yml` in the repository and confirmed the workflow was already correct. No changes were made. |
| Python 3.11 support is not demonstrated by the supplied workflow. | **Noise** | The comment was speculative because it was based only on the workflow file and not on the repository as a whole. It did not identify a verified problem. | Reviewed the workflow and project configuration. No evidence showed that Python 3.11 was unsupported, so no action was taken. |
| The workflow name `CI` may be too broad because it only runs tests. | **Noise** | Installing dependencies and running automated tests is a standard continuous integration workflow for this project. | Rejected the suggestion and kept the existing workflow name unchanged. |

## AI Security Mini-Review

**Security review date: August 2, 2026**

This was a read-only security review, and no source files were modified during the review.

| Finding | File evidence | Grade: Valid / False Positive / Noise | Reason | Next action |
| ------- | ------------- | ------------------------------------- | ------ | ----------- |
| Missing authentication and authorization | `app/main.py:52`; `README.md:5` | Valid | Authentication is absent, so any client that reaches the API can perform all task operations; this is a real risk if network-exposed but an intentionally accepted limitation for this local coursework project. | No authentication code change is required for the current coursework scope; authentication and per-task authorization would be required before shared or production deployment. |
| Unbounded user-controlled fields and tags | `app/models.py:51`; `app/models.py:108` | Valid | Description and assignee lengths, individual tag lengths, and the number of tags are unrestricted, which could allow excessive resource usage. | Propose course-appropriate limits for descriptions, assignees, tag length, and tag count, and add boundary tests if a fix is approved. |
| Unbounded in-memory storage and full-list responses | `app/storage.py:8`; `app/storage.py:68`; `app/main.py:52` | Valid | Tasks remain in an unbounded module-level dictionary, and `GET /tasks` returns the complete collection, which could exhaust memory or amplify responses. | Document the current capacity limitation; before broader use, define pagination, result limits, request throttling, and an appropriate storage strategy. |
| Permissive CORS configuration | `app/main.py:24`; `frontend/index.html:725` | Valid | Every origin, method, and header is allowed with credentials; this is acceptable for local learning use but inappropriate for production deployment. | For local-only use, consider disabling credentials; for hosted use, configure an explicit origin allowlist and an environment-specific frontend API URL. |
| Reflected task IDs in 404 responses | `app/main.py:130`; `app/main.py:176`; `app/main.py:243` | Noise | The task ID is returned in a JSON response, no sensitive information is exposed, and no realistic security exploit was demonstrated. | Treat this only as an API design improvement by validating IDs or returning a fixed `Task not found` message if a change is later approved. |

## Manual security check

I manually reviewed how the frontend renders user-controlled content to verify that it is displayed safely. To locate every use of the escaping helper, I ran:

```bash
grep -n "escapeHtml" frontend/index.html
```

I then inspected each matching location and confirmed that task titles, descriptions, assignees, tags, and due dates are passed through `escapeHtml()` before being inserted into the page with `innerHTML`. I also created a task containing HTML-like input and verified that the frontend displayed the content as plain text rather than interpreting it as HTML.

This matters because safely rendering user-controlled input helps prevent stored cross-site scripting (XSS) vulnerabilities.

## One AI output I rejected or corrected

During the final AI code review, Codex claimed that `.github/workflows/ci.yml` contained several YAML indentation problems. It said the workflow steps were not indented beneath `steps:`, that `python-version` was not nested beneath `with:`, and that the commands inside the multiline `run` block were incorrectly indented. I did not accept these findings as-is because the workflow content had been copied into the prompt, where formatting could have been lost. Instead, I inspected the actual repository file and ran `nl -ba .github/workflows/ci.yml` to verify the indentation line by line. I also checked the passing GitHub Actions run recorded in the release evidence. The real workflow was correctly formatted, so I graded the AI comments as wrong, rejected the recommendations, and made no changes to the workflow.

## Three AI usage rules

1. **Never paste:** Real customer data, personal information, production data, credentials, API keys, tokens, or any confidential information into an AI tool.

2. **Always verify:** Inspect AI-generated changes, review the proposed diff, run the appropriate tests or manual checks, and make sure I understand the final implementation before accepting it.

3. **Record AI contributions by:** Documenting the prompts I used, the AI output, what I accepted or rejected, and the verification I performed so every significant AI-assisted change remains transparent and traceable.

## Ownership statement

I am confident submitting this repository because I personally reviewed every major change before accepting it and verified the final result by running the application, pytest, GitHub Actions, Docker, and manual browser testing. AI helped me draft code, review documentation, and identify possible issues, but I always inspected the changes, tested them myself, and decided what to keep or reject. I rejected AI suggestions when they were based on incorrect assumptions or didn't match my project's actual behavior, and I corrected the documentation whenever it didn't reflect what I had verified. After building, testing, debugging, and reviewing every part of this project, I understand how the application works, why each major decision was made, and what its current limitations are.