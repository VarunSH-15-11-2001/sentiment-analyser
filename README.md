Here’s a clean, copy-paste README for your **sentiment-analyzer** (parent) repo.

---

# Sentiment Analyzer (Full Stack)

A tiny full-stack app for 3-class sentiment analysis (Positive / Neutral / Negative).

* **Backend**: FastAPI + Transformers (Hugging Face), endpoints for single and batch analysis.
* **Frontend**: React (Vite) + Tailwind, Dockerized with Nginx, runtime-configurable API base.
* **One-command local run**: Docker Compose builds and runs both services.

## Repo layout

```
sentiment-analyzer/
├─ docker-compose.yml          # runs both services
├─ sentiment-api/              # FastAPI backend (submodule)
└─ sentiment-ui/               # React frontend (submodule)
```

## Quick start (local)

### 1) Clone with submodules

```bash
git clone --recurse-submodules <YOUR_PARENT_REPO_URL> sentiment-analyzer
cd sentiment-analyzer
# (if you forgot --recurse-submodules)
# git submodule update --init --recursive
```

### 2) Run with Docker Compose

```bash
docker compose up --build
```

* Frontend: [http://localhost:3000](http://localhost:3000)
* Backend:  [http://localhost:8080](http://localhost:8080)

The frontend talks to the backend via the compose network (`API_BASE=http://api:8080`), and you can still hit the backend directly on `localhost:8080`.

## API (backend)

Base URL (local): `http://localhost:8080`

* `GET /openapi.json` – OpenAPI schema (handy as a health check on Cloud Run).
* `GET /check_health` – Health status (returns model name).
* `POST /analyze` – Single text.

  * Body: `{"text": "I absolutely love this!"}`
* `POST /batch` – Multiple texts.

  * Body: `{"items":[{"id":"1","text":"good"}, {"id":"2","text":"bad"}]}`

### cURL examples

```bash
# Health
curl -i http://localhost:8080/check_health

# Single analyze
curl -s -X POST http://localhost:8080/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"This is amazing"}' | jq

# Batch analyze
curl -s -X POST http://localhost:8080/batch \
  -H "Content-Type: application/json" \
  -d '{"items":[{"id":"1","text":"great job"},{"id":"2","text":"this is awful"}]}' | jq
```

## Frontend

* Open [http://localhost:3000](http://localhost:3000).
* Top-right input lets you set the **API base URL** (persisted in localStorage).
  For local dev leave it as `http://localhost:8080`.

Features:

* Single query with confidence bars.
* Batch mode (one text per line) with on-screen results and optional CSV download.
* History pane (last 50, stored in localStorage).
* Displays model name and latency.

## Configuration

* **Ports**: Frontend :3000 (Nginx inside container listens on 80), Backend :8080.
* **CORS**: Backend allows `*` by default.
* **Frontend runtime API base**:

  * Docker image reads `API_BASE` env at container start (via `/config.js`).
  * In `docker-compose.yml` it’s set to `http://api:8080`.

## Deploy notes (brief)

* **Render**: Deploy each repo as a Docker web service. Set frontend `API_BASE` to the backend’s public URL.
* **GCP Cloud Run**: Use the service URL shown for your region. If `/check_health` behaves oddly behind GFE, you can use `/openapi.json` as the health path.
* **Persistent model cache** (optional for faster cold starts):

  * Mount a volume at `/root/.cache/huggingface` for the backend.

## Troubleshooting

* Frontend loads but looks unstyled → ensure Tailwind built (in our Dockerfile it’s handled).
* Frontend can’t reach API → verify the top-right **API base** and that backend is on :8080.
* Submodules appear empty after clone → run:

  ```bash
  git submodule update --init --recursive
  ```
