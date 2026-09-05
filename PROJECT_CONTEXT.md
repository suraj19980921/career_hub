# GovCareer Hub — Project Context

## Project

GovCareer Hub is an Indian government jobs and exam information platform.

## Primary goal

Build a useful public platform where users can discover government jobs, exams, results, admit cards, answer keys, cutoffs, syllabus, and previous-year papers.

## Monetization

Google AdSense is the primary monetization strategy. Future support may include affiliate links, sponsored listings, and premium features.

## Development approach

We use vertical-slice development. Each requested feature is considered through the full user-facing path before moving to another feature:

1. Understand the screen and user flow.
2. Define frontend requirements.
3. Identify required data.
4. Design only the required database changes.
5. Design backend APIs.
6. Implement backend.
7. Implement frontend.
8. Test the complete feature.
9. Do not build future features unless explicitly requested.

Do not attempt to build the entire application at once.

## Technology stack

### Backend

- Python
- Django
- Django REST Framework
- PostgreSQL

### Frontend

- React
- Vite
- Bootstrap 5
- React Router
- Axios

### Development

- Git
- Environment variables
- Docker will be added as required

## Product development order

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

## UI principles

- Mobile-first
- Clean and modern
- Trustworthy government-career focused design
- Responsive
- Fast loading
- SEO-friendly
- Advertisement space should be considered without hurting UX

## Coding principles

- Use clean, maintainable code.
- Follow Django and React best practices.
- Avoid overengineering.
- Do not create unnecessary abstractions.
- Do not create database tables until required by an implemented feature.
- Keep business logic out of overly large views/components.
- Do not modify unrelated code.
- Explain architectural changes before making major changes.
- Run relevant tests or validation commands after implementation.
- Report changed files and a short summary after completing a task.

## Current status

No application has been implemented yet. The project is starting from the project foundation.
