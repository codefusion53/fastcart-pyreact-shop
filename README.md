# FastAPI + React Ecommerce

A full-stack ecommerce app built with a **FastAPI + MongoDB** backend and a
**Vite + React** frontend (React Router, React Query, Tailwind CSS). A Docker
Compose setup runs MongoDB plus a Mongo Express admin UI for local development.

> **Status:** Work in progress. The backend exposes full CRUD for products and
> users backed by MongoDB; the frontend has routing, data fetching, and a
> product listing/detail UI under active development.

## Tech stack

| Layer     | Tools                                                              |
| --------- | ------------------------------------------------------------------ |
| Backend   | FastAPI, Uvicorn, Motor (async MongoDB driver), Pydantic           |
| Database  | MongoDB (+ Mongo Express UI)                                        |
| Frontend  | React 18, Vite, React Router, TanStack React Query, Tailwind CSS, Splide |
| Tooling   | Docker Compose, python-dotenv                                      |

## Project structure

```
.
├── docker-compose.yml          # MongoDB + Mongo Express services
├── .env.example                # Copy to .env and fill in
├── backend/
│   ├── requirements.txt
│   └── src/
│       ├── main.py             # ASGI entrypoint (uvicorn)
│       ├── app.py              # App factory: CORS + router registration
│       ├── config/             # Env loading + MongoDB URI assembly
│       ├── database/           # Motor async client
│       ├── middlewares/        # CORS middleware
│       ├── models/             # Pydantic models (User, Product, common base)
│       └── routers/            # API routes (products, users)
└── frontend/
    ├── package.json
    ├── tailwind.config.cjs
    └── src/
        ├── api/                # API base URL
        ├── services/           # Data-fetching services
        ├── components/         # Header, Footer, Layout, ProductCard
        ├── pages/              # Home, Product, About
        └── styles/
```

## Prerequisites

- Python 3.10+
- Node.js 18+
- Docker and Docker Compose

## Getting started

### 1. Environment variables

Copy the example file and adjust as needed:

```bash
cp .env.example .env
```

| Variable        | Purpose                                                        |
| --------------- | -------------------------------------------------------------- |
| `MONGO_USERNAME`, `MONGO_PASSWORD` | MongoDB credentials                         |
| `MONGO_DB_HOST` | `localhost` on host, `mongo` inside Docker Compose             |
| `MONGO_DB_PORT` | MongoDB port (default `27017`)                                 |
| `MONGO_DB_NAME` | Database name (must not be empty)                              |
| `CORS`          | Comma-separated allowed frontend origins                       |
| `VITE_API_URL`  | Base URL the React app uses to reach the API                   |

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

API at `http://localhost:8000`, interactive docs at `http://localhost:8000/docs`.

### 4. Run the frontend

```bash
cd frontend
npm install
npm run dev
```

Vite serves the app at `http://localhost:5173`.

## API overview

Resource ids are MongoDB `ObjectId`s. Updates are partial — send only the
fields you want to change.

| Method | Endpoint         | Description                | Success |
| ------ | ---------------- | -------------------------- | ------- |
| GET    | `/products/`     | List products              | 200     |
| GET    | `/products/{id}` | Get a single product       | 200     |
| POST   | `/products/`     | Create a product           | 201     |
| PUT    | `/products/{id}` | Update a product (partial) | 200     |
| DELETE | `/products/{id}` | Delete a product           | 204     |

The same set of routes exists for `/users/`. Full, auto-generated docs live at
`/docs` (Swagger UI) and `/redoc`.

## Roadmap

- [ ] Product create/edit forms in the frontend
- [ ] User authentication (registration, login, JWT)
- [ ] Cart and checkout flow
- [ ] Tests and CI

## License

Add a license of your choice (e.g. MIT) here.
