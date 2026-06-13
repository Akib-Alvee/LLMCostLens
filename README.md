# LLMCostLens

LLMCostLens is a monorepo with a FastAPI backend and a React + Vite frontend.

## Repository structure

```text
.
├── backend/
│   ├── app/
│   ├── scripts/
│   └── tests/
└── frontend/
    ├── public/
    └── src/
```

## Backend

Prerequisites: Python 3.11 or newer.

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

The API runs at `http://localhost:8000`. Interactive API documentation is
available at `http://localhost:8000/docs`.

Run backend tests with:

```bash
cd backend
source .venv/bin/activate
pytest
```

Check and format backend code with:

```bash
cd backend
source .venv/bin/activate
ruff check app tests
black --check app tests
black app tests
```

Create and apply database migrations from `backend/`:

```bash
alembic revision --autogenerate -m "message"
alembic upgrade head
```

Seed demo users and model pricing after applying migrations:

```bash
python -m scripts.seed_users
python -m scripts.seed_model_pricing
```

The demo API keys are `demo-user-1-key` and `demo-user-2-key`. Only their
SHA256 hashes are stored in the database.

## Frontend

Prerequisites: Node.js 20.19+ or 22.12+ and npm.

```bash
cd frontend
npm install
npm run dev
```

The frontend runs at `http://localhost:5173`.

Additional frontend commands:

```bash
npm run build
npm run lint
npm run format
```
