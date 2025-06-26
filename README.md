# BottomLine A/B Testing MVP

This project adds a minimal A/B testing setup consisting of a WordPress plugin, a FastAPI backend and a React dashboard.

## Install

### Plugin
Copy the `wp-plugin` folder to your WordPress `plugins` directory and activate **BottomLine AB Tests** in the admin.

### Backend
```bash
cd ab-tests-backend
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn pydantic
uvicorn main:app --reload --port 8001
```

### Frontend
Inside `frontend` run:
```bash
npm install
npm run dev
```

## Usage
1. Activate the plugin and ensure tracking is enabled in the settings page.
2. Visit a page containing an element with `data-ab-id="cta"`. The JS client will assign a variant and track views and clicks.
3. View results at `http://localhost:8001/results/cta_test` or navigate to `/dashboard/cta_test` in the React frontend.
4. Press "Apply Winner" to publish the winning variant.

## Testing
Run backend unit tests with:
```bash
pytest
```

The default repository tests may fail without optional dependencies. These can be installed manually if required.
