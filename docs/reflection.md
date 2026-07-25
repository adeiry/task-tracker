# Reflection

## What Went Well

Planning the implementation before writing code reduced unnecessary changes and made the development process more predictable. Using AI to inspect the project before editing helped identify the minimum required modifications while preserving the existing architecture.

Writing automated tests alongside each feature improved confidence in the implementation and made regression testing straightforward.

---

## Challenges

The biggest challenge was extending the existing application without introducing unnecessary complexity. Care was also required to preserve backward compatibility while adding optional due dates and tags.

Frontend filtering logic became more complex as additional filters were introduced.

---

## AI Usage

AI was used throughout the project to:

- inspect the existing architecture
- plan implementation
- generate implementation suggestions
- generate automated tests
- review completed work
- verify feature completeness

All AI-generated code and suggestions were reviewed manually before being accepted.

---

## Lessons Learned

This project reinforced the importance of:

- planning before implementation
- preserving backward compatibility
- writing tests for new features
- verifying behavior manually
- using AI as a development assistant rather than replacing developer judgment

## Additional Work

After completing the required project features, I added two optional improvements.

First, I exposed the existing backend task deletion functionality in the frontend. This completed the CRUD workflow from the user interface and required confirmation handling, API integration, UI updates, and error handling.

Second, I completed a focused frontend-polish pass. I improved task cards, spacing, buttons, filters, form states, tag and due-date presentation, and drag-and-drop feedback. I intentionally avoided adding a new framework or changing backend behavior so that the improvements remained low-risk and within the project scope.

These additions improved the usability and presentation of the application while preserving the tested backend behavior.