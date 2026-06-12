# AGENTS.md

## Scope

These instructions apply to the entire LLMCostLens repository.

## Architecture

- `backend/` contains the FastAPI application.
- `frontend/` contains the React + Vite application.
- Keep API, persistence, provider, and service concerns in their existing
  backend package boundaries.
- Keep reusable frontend code under `frontend/src/`.

## Development guidelines

- Do not commit secrets or local `.env` files.
- Add backend dependencies to `backend/requirements.txt`.
- Add frontend dependencies to `frontend/package.json`.
- Keep business logic out of FastAPI route handlers.
- Add or update tests with behavior changes.
- Run relevant formatting, linting, and tests before finishing a change.

## Verification

Backend:

```bash
cd backend
pytest
```

Frontend:

```bash
cd frontend
npm run lint
npm run build
```

