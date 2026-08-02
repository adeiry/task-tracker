# Personal AI Coding Playbook

## 1. When I reach for AI first

Every AI-assisted task follows the same workflow: **ask, inspect, run, verify with real evidence, then refine**.

I reach for AI to implement an already-specified feature or to generate boilerplate (docstrings, Dockerfiles, CI workflows, test scaffolding). During the mid-course project, I used AI to implement the due date, tag, filtering, and validation features, then verified each one against the project requirements before accepting the changes.

My goal is a narrowly scoped, testable change I can verify against my own spec—not an AI-generated decision about what the product should do.

## 2. When I do not reach for AI

I do not rely on AI to decide product behavior, architecture, priorities, or when work is ready to ship. Those decisions stay mine. During mid-course planning, AI compared due dates, tags, comments, and activity history, but I selected due dates and tags and recorded the tradeoffs in the mini ADR before implementation.

One personal boundary applies regardless of project size: I will never paste real customer, personal, production, regulated, or confidential data—or credentials, API keys, tokens, or private service info—into an AI tool. This isn't based on a course incident; it's a career-long rule.

## 3. My non-negotiables

- AI prepares the change; I decide whether to accept it. Reviewing the Kanban drag-and-drop logic, I flagged event-handling code I couldn't fully explain instead of accepting it as-is.
- I review every diff before it's committed, and only commit once I've decided it's ready. I inspected AI-generated backend modules and corrected wrong assumptions before merging; before finalizing a refactor, I ran the full before/after behavior contract and confirmed zero regressions first.
- I do not accept claims that code "should work"—I want evidence. My two Break Tests proved this: I broke blank-tag validation and overdue filtering on purpose, confirmed each test failed, restored the fix, and reran the full 60-test suite before trusting either behavior again.

## 4. My review rules

I verify AI suggestions using evidence rather than explanations.

- **Tests:** I ask for or run the real pytest output, not a summary—my verification report records actual run counts ("60 passed") and the literal commands I ran.
- **Docker:** A clean `docker build` doesn't prove the container works: I built the image, ran it, hit `/health` myself, and confirmed it runs as a non-root user without `--reload` before accepting it.
- **CI:** Workflow YAML looking right isn't the same as it running right: I reviewed each step, then confirmed in the GitHub Actions tab that it actually passed before calling the task complete.
- **Frontend:** I verify UI behavior in the browser with DevTools, not screenshots or descriptions—on the Kanban board, that meant checking task rendering, PATCH requests, and failed-move rollback directly.
- **Documentation:** I audited the API documentation twice. The second review caught a regression the first fix introduced, reinforcing one of my biggest lessons: **"fixed once" does not mean "verified forever."**

## 5. What I am still figuring out

- How much duplicated explanation across docstrings, route decorators, and API docs I should tolerate before insisting on one source of truth.
- Whether automated tests on the generated OpenAPI schema would catch the documentation regressions I currently catch by hand.
- How to handle branch reviews when long-lived branches carry work from previous modules—one review mixed old and current feature work and became needlessly hard.

## Decision Card

- **For a new feature:** I write one detailed prompt describing the expected behavior, constraints, and verification steps before asking AI to generate code.
- **For a code review:** I ask for a structured review with evidence and actionable findings instead of rewritten code.
- **For debugging:** I ask for the root cause and the smallest fix, then verify by rerunning the failing case and the full test suite.
- **For infrastructure:** I set hard constraints first (no `:latest` tags, no secrets, non-root containers, no `--reload` in production) before reviewing the diff.
- **I will never paste:** customer, personal, production, regulated, or confidential data, or credentials/tokens (full list in Section 2) into an AI tool.
- **My one rule:** Show me the diff and the real verification—then I decide what gets committed.

## Revisit

I will re-read this playbook in **30 days** and update it if my AI workflow, verification habits, or review standards have changed.
