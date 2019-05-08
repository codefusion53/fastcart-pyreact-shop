# FastAPI + React Ecommerce

A full-stack ecommerce starter built with a **FastAPI + MongoDB** backend and a
**Vite + React** frontend. It ships with a Docker Compose setup for MongoDB (plus
a Mongo Express admin UI) so you can get a local environment running quickly.

> **Status:** Early-stage scaffold. The backend exposes a basic product/user
> router structure wired to MongoDB; the frontend is the Vite + React starter
> ready to be built out. See the [Roadmap](#roadmap) for what's planned.

## Tech stack

| Layer     | Tools                                                        |
| --------- | ----------------------------------------------------------- |
| Backend   | FastAPI, Uvicorn, Motor (async MongoDB driver), Pydantic    |
| Database  | MongoDB (+ Mongo Express UI)                                 |
| Frontend  | React 18, Vite                                               |
| Tooling   | Docker Compose, python-dotenv                               |

## Project structure

```
.
├── docker-compose.yml      # MongoDB + Mongo Express services
├── backend/
│   ├── requirements.txt
│   └── src/
│       ├── main.py         # ASGI entrypoint (app = create_app())
│       ├── app.py          # FastAPI app factory + router registration
│       ├── config/         # Env loading + MongoDB URI assembly
│       ├── database/       # Motor async client
│       ├── models/         # Pydantic models (User, Product, common base)
│       └── routers/        # API routes (products, users)
└── frontend/
    ├── index.html
    ├── package.json
    └── src/                # React app (App.jsx, main.jsx)
```

## Prerequisites

- Python 3.10+
- Node.js 18+
- Docker and Docker Compose

## Getting started

### 1. Environment variables

The backend and Docker Compose read configuration from a `.env` file in the
project root. Create one with:

```env
MONGO_USERNAME=admin
MONGO_PASSWORD=changeme
MONGO_DB_HOST=localhost
MONGO_DB_PORT=27017
MONGO_DB_NAME=ecommerce
```

> When the backend runs **inside** Docker, set `MONGO_DB_HOST=mongo` (the
> service name). When it runs on your host machine against the Dockerized DB,
> use `localhost`.

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
uvicorn main:app --reload
```

The API is then available at `http://localhost:8000`, with interactive docs at
`http://localhost:8000/docs`.

> **Note:** Start the server with `uvicorn main:app` (run from `backend/src`),
> not `python main.py` — FastAPI apps are served by an ASGI server.

### 4. Run the frontend

```bash
cd frontend
npm install
npm run dev
```

Vite serves the app at `http://localhost:5173`.

## API overview

| Method | Endpoint         | Description          |
| ------ | ---------------- | -------------------- |
| GET    | `/products/`     | List products        |
| GET    | `/products/{id}` | Get a single product |
| POST   | `/products/`     | Create a product     |
| PUT    | `/products/{id}` | Update a product     |
| DELETE | `/products/{id}` | Delete a product     |

Full, always-up-to-date docs are auto-generated at `/docs` (Swagger UI) and
`/redoc`.

## Roadmap

- [ ] Flesh out the user router (registration, auth, JWT)
- [ ] Persist real product data and validation via Pydantic models
- [ ] Build the React storefront (product list, cart, checkout)
- [ ] Add tests and CI
- [ ] Containerize the backend and frontend in Compose

## License

Add a license of your choice (e.g. MIT) here.
