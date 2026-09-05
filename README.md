# GovCareer Hub

GovCareer Hub is an Indian government jobs and exam information platform.

## Repository layout

- `backend/` — Django and Django REST Framework API.
- `frontend/` — React and Vite web application.
- `AGENTS.md` — permanent development instructions.
- `PROJECT_CONTEXT.md` — product and technical context.

## Local setup

### Backend

1. Create and activate a Python virtual environment.
2. Install dependencies: `python -m pip install -r requirements/development.txt`
3. Copy `.env.example` to `.env` and set local values. Django loads this file locally.
4. Run migrations: `python manage.py migrate`
5. Start the server: `python manage.py runserver`

### Frontend

1. Copy `.env.example` to `.env`.
2. Install dependencies: `npm install`
3. Start the development server: `npm run dev`

The development API health endpoint is available at `/api/health/`.
