# WebFix

WebFix is an AI-powered Conversion Rate Optimization (CRO) auditing app.

It combines a FastAPI backend with a React/Vite frontend to inspect landing pages and surface actionable suggestions for improving conversions. Submit a URL and the service uses OpenAI GPT-4.1 to evaluate the page, capture a screenshot, cache results in Redis, and optionally email deep reports via AWS SES.

<!-- TODO: Add build/status badges -->

## Features

- Analyze any public URL and receive CRO recommendations
- Capture page screenshots with Playwright
- Cache generated reports in Redis for quick retrieval
- Send detailed reports by email after verification

## Installation

### Backend (Python 3.10+)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt

# optional: screenshot support
pip install playwright
playwright install
```

### Frontend

```bash
cd frontend
npm install
```

## Quick Start

### Start the backend (http://127.0.0.1:8000)

```bash
uvicorn backend.main:app --reload
```

### Start the frontend (http://localhost:5173)

```bash
cd frontend
npm run dev
```

## Configuration

| Variable | Description |
| --- | --- |
| OPENAI_API_KEY | OpenAI key used by GPT service |
| AWS_ACCESS_KEY_ID | AWS credential for SES |
| AWS_SECRET_ACCESS_KEY | AWS credential for SES |
| AWS_DEFAULT_REGION | AWS SES region |
| JWT_SECRET_KEY | Secret used for email verification tokens |
| REDIS_HOST | Redis server host |
| REDIS_PORT | Redis server port |
| REDIS_USERNAME | Redis username |
| REDIS_PASSWORD | Redis password |

## Usage

### Health check

```bash
curl http://127.0.0.1:8000/
```

### Generate CRO report

```bash
curl -X POST http://127.0.0.1:8000/analyze-url \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com","report_type":"basic","email":"user@example.com"}'
```

### Response

```json
{
  "output": "{ ...CRO report JSON... }",
  "screenshot_base64": "...",
  "is_cached": false
}
```

After verifying email links, `GET /verify-email?token=<jwt>` sends deep reports.

## Testing

### Backend

```bash
pytest backend/tests
```

### Frontend

```bash
cd frontend
npm run lint
```

## Development / Contributing

1. Fork and clone the repository.
2. Follow the installation steps and run the backend and frontend locally.
3. Use feature branches and open pull requests.

## Architecture

- **FastAPI service** orchestrates OpenAI GPT‑4.1, Redis caching, AWS SES email, and Playwright screenshots.
- **React/Vite frontend** submits URLs, displays reports, and screenshots.
- **Redis** stores generated reports for quick retrieval.


