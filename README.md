# FastAPI + React Ecommerce

A full-stack ecommerce app with a **FastAPI + MongoDB** backend and a
**Vite + React** frontend (React Router, React Query, Redux, Tailwind CSS).
Docker Compose runs MongoDB plus a Mongo Express admin UI for local dev.

> **Status:** Work in progress. The backend exposes full CRUD for products and
> users under `/api/v1`, plus JWT login/signup under `/auth`. The frontend has
> routing, data fetching, Redux state, a login page, and a product UI in progress.

## Tech stack

| Layer     | Tools                                                                       |
| --------- | --------------------------------------------------------------------------- |
| Backend   | FastAPI, Uvicorn, Motor (async MongoDB), Pydantic, python-jose, passlib      |
| Database  | MongoDB (+ Mongo Express UI)                                                 |
| Frontend  | React 18, Vite, React Router, TanStack React Query, Redux, Tailwind CSS, Splide |
| Tooling   | Docker Compose, python-dotenv                                               |

## Project structure

```
.
├── docker-compose.yml          # MongoDB + Mongo Express
├── .env.example                # Copy to .env and fill in
├── backend/
│   ├── requirements.txt
│   └── src/
│       ├── main.py             # ASGI entrypoint (uvicorn)
│       ├── app.py              # App factory: CORS + routers
│       ├── config/             # Env loading + MongoDB URI
│       ├── database/           # Motor async client
│       ├── middlewares/        # CORS
│       ├── auth/               # JWT login/signup (passlib + python-jose)
│       ├── models/             # Pydantic models
│       └── routers/            # /api/v1 product & user routes
└── frontend/
    └── src/                    # api, services, components, pages, hooks, redux, auth, styles
```

## Prerequisites

- Python 3.10+
- Node.js 18+
- Docker and Docker Compose

## Getting started

### 1. Environment

```bash
cp .env.example .env
```

| Variable                      | Purpose                                          |
| ----------------------------- | ------------------------------------------------ |
| `MONGO_USERNAME` / `MONGO_PASSWORD` | MongoDB credentials                        |
| `MONGO_DB_HOST`               | `localhost` on host, `mongo` inside Compose      |
| `MONGO_DB_PORT` / `MONGO_DB_NAME` | MongoDB port / database name (non-empty)     |
| `CORS`                        | Comma-separated allowed frontend origins         |
| `SECRET_KEY`                  | JWT signing key (`openssl rand -hex 32`)         |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime                            |
| `VITE_API_URL`                | API host for the React app (host only, no `/api/v1`) |
| `VITE_TOKEN_KEY`              | localStorage key for the JWT (default `access_token`) |

### 2. Start MongoDB

```bash
docker compose up -d
```

- MongoDB → `localhost:27017`
- Mongo Express UI → `http://localhost:8081`

### 3. Run the backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

cd src
uvicorn main:app --reload         # or: python main.py
```

API at `http://localhost:8000`, docs at `http://localhost:8000/docs`.

### 4. Run the frontend

```bash
cd frontend
npm install
npm run dev
```

Vite serves the app at `http://localhost:5173`.

## API overview

Product/user routes are prefixed with `/api/v1`. Ids are MongoDB `ObjectId`s,
and updates are partial (send only the fields you want to change). Reads are
public; **create/update/delete require a Bearer token** from `/auth/login`.

| Method | Endpoint                | Description                | Success |
| ------ | ----------------------- | -------------------------- | ------- |
| GET    | `/api/v1/products/`     | List products              | 200     |
| GET    | `/api/v1/products/{id}` | Get a product              | 200     |
| POST   | `/api/v1/products/`     | Create a product           | 201     |
| PUT    | `/api/v1/products/{id}` | Update a product (partial) | 200     |
| DELETE | `/api/v1/products/{id}` | Delete a product           | 204     |
| POST   | `/auth/signup`          | Register a user            | 200     |
| POST   | `/auth/login`           | Log in, returns a JWT      | 200     |
| GET    | `/auth/me`              | Current user (requires JWT)| 200     |

The same product routes exist for `/api/v1/users/`. Auto-generated docs live at
`/docs` and `/redoc`.

## Roadmap

- [x] Protect write routes with the JWT dependency
- [x] Align the auth user record with the `User`/`UserInDB` model
- [ ] Product create/edit forms in the frontend
- [ ] Cart and checkout flow
- [ ] Tests and CI

## License

Add a license of your choice (e.g. MIT) here.
