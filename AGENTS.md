# GovCareer Hub Development Instructions

## Project purpose

GovCareer Hub is an Indian government jobs and exam information platform. Build it as a useful, trustworthy public service where people can find government jobs, exams, results, admit cards, answer keys, cutoffs, syllabus, and previous-year papers.

## Development workflow

Use vertical-slice development. Work on one requested feature at a time and complete it end to end before starting another.

For every feature:

1. Understand the screen and user flow.
2. Define frontend requirements.
3. Identify the data the feature needs.
4. Design only the required database changes.
5. Design backend APIs.
6. Implement the backend.
7. Implement the frontend.
8. Test the complete feature.
9. Do not build future features unless explicitly requested.

Do not attempt to build the whole application at once.

## Technology choices

- Backend: Python, Django, Django REST Framework, PostgreSQL.
- Frontend: React, Vite, Bootstrap 5, React Router, Axios.
- Development: Git and environment variables. Add Docker only when required.

## Coding standards

- Keep code clean, maintainable, and appropriately simple.
- Follow Django, Django REST Framework, React, and Vite best practices.
- Avoid overengineering, speculative code, and unnecessary abstractions.
- Do not add database tables until an implemented feature requires them.
- Keep business logic out of oversized Django views and React components.
- Do not modify unrelated code or overwrite existing user changes.
- Explain architectural changes before making major changes.
- Use environment variables for secrets and environment-specific configuration; never commit secrets.
- Prefer mobile-first, responsive, fast-loading, accessible, and SEO-friendly UI.
- Reserve advertisement placements thoughtfully without degrading usability or trust.

## Product order

Implement product areas in this order unless the user explicitly changes it:

1. Project foundation
2. Shared UI foundation
3. Homepage
4. Jobs listing
5. Job details
6. Exams listing
7. Exam details
8. Results
9. Admit cards
10. User authentication and dashboard
11. Additional features incrementally

## Completion checklist

After implementing a task:

1. Run relevant tests, linters, builds, or validation commands.
2. Report the files changed.
3. Give a brief summary of what was implemented and how it was validated.

