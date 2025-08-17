# WebFix

WebFix is a web application that generates conversion rate optimization (CRO) reports for any URL. A FastAPI backend collects a screenshot, consults OpenAI for a report and caches results in Redis. The React frontend lets users request and view reports with a modern Tailwind CSS interface.

## Features
- Analyze URLs and return CRO reports powered by OpenAI
- Optional deep reports with email verification via AWS SES
- Screenshot capture and caching of previous reports
- Responsive React interface with Tailwind CSS
- Basic Redis caching layer

## Tech Stack
- **Backend:** FastAPI, Redis, boto3, JWT
- **Frontend:** React (TypeScript), Tailwind CSS, Axios
- **Testing:** Pytest, Jest (via `npm test`)
- **CI/CD:** GitHub Actions
- **Optional:** Docker for containerized deployment

## Installation

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Frontend
```bash
cd frontend
npm install
```

## Usage

### Backend API
Start the FastAPI server:
```bash
uvicorn backend.main:app --reload
```

Example request:
```bash
curl -X POST http://127.0.0.1:8000/analyze-url \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://example.com", "report_type": "basic"}'
```

### Frontend
Start the development server:
```bash
cd frontend
npm run dev
```
Open your browser at `http://localhost:5173` and submit a URL.

## Testing
Run backend tests:
```bash
pytest
```
Run frontend tests:
```bash
cd frontend
npm test
```

## Deployment

### Local with Docker
```bash
docker build -t webfix-backend backend
# optional: docker build -t webfix-frontend frontend
```

### CI/CD
GitHub Actions workflows can be configured to run linting, tests and deployments. Add workflows under `.github/workflows` to automate builds and deploy to cloud providers such as AWS or Azure.

## Contributing
1. Fork the repository
2. Create a branch for your feature or bugfix
3. Submit a pull request with a clear description

## License

This project is licensed under the [MIT License](LICENSE).
