WebFix
AI‑powered CRO auditing app with a FastAPI backend and React/Vite frontend.

Badges
TODO: Add build/status badges.

**Installation:**
---
# Backend (Python 3.10+)
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
# optional: screenshot support
pip install playwright
playwright install

# Frontend
cd frontend
npm install
---

**Quick Start:**
---
# Start backend (default http://127.0.0.1:8000)
uvicorn backend.main:app --reload

# Start frontend (default http://localhost:5173)
cd frontend
npm run dev
---

**Configuration**:
---
Variable	Description
OPENAI_API_KEY	OpenAI key used by GPT service
AWS_ACCESS_KEY_ID	AWS credential for SES
AWS_SECRET_ACCESS_KEY	AWS credential for SES
AWS_DEFAULT_REGION	AWS SES region
JWT_SECRET_KEY	Secret used for email verification tokens
REDIS_HOST	Redis server host
REDIS_PORT	Redis server port
REDIS_USERNAME	Redis username
REDIS_PASSWORD	Redis password
---

**Usage:**
# Health check
---
curl http://127.0.0.1:8000/
---
# Generate CRO report
curl -X POST http://127.0.0.1:8000/analyze-url \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com","report_type":"basic","email":"user@example.com"}'
---

**Response:**
{
  "output": "{ ...CRO report JSON... }",
  "screenshot_base64": "...",
  "is_cached": false
}

After verifying email links, GET /verify-email?token=<jwt> sends deep reports.


**Testing**:
---
# Backend unit tests
pytest backend/tests
---
# Frontend lint
cd frontend
npm run lint
---

**Development / Contributing**
---
Fork and clone the repo.

Follow installation steps and run backend/frontend locally.

Use feature branches and open pull requests.
---
**Architecture**
---
FastAPI service orchestrates OpenAI GPT‑4.1, Redis caching, AWS SES email and Playwright screenshots.

React/Vite frontend submits URLs, displays reports and screenshots.

Redis stores generated reports for quick retrieval.
---
