# BottomLine A/B Tests

This repository contains a minimal A/B testing stack for WordPress.

## Quick Start

1. Install Docker and Docker Compose.
2. Run `docker-compose up --build` from the repository root.
3. Visit `http://localhost:8080` to finish WordPress setup.
4. Log in to WordPress admin and activate the **BottomLine AB Tests** plugin.
5. Open the "A/B Test Sample Page" to see the CTA modified.
6. View results at `http://localhost:3000/dashboard/cta_test` when the React app is served or by visiting the backend API at `http://localhost:8000/results/cta_test`.

## WordPress Plugin

The plugin enqueues a script that assigns visitors to variant **A**, **B**, or **C** and tracks clicks via the backend API. A settings page under **Settings → BottomLine AB Tests** lets you disable tracking. A sample page is automatically created on activation containing:

```html
<button id="cta-test-btn" data-ab-id="cta-test-btn">Join Now</button>
```

This selector is used by the JS client for the experiment.

## Backend

The FastAPI backend stores events in SQLite. Endpoints:

- `POST /events` – record view/click events
- `GET /results/cta_test` – aggregated results
- `PUT /results/cta_test/publish` – store the winning variant

## Frontend Dashboard

Navigate to `/dashboard/cta_test` in the React app to see live statistics. The table updates every 10 seconds and lets you apply the winning variant.

## Testing

- Python tests: `pytest`
- JS tests: `npm test` inside `static/`

If Docker services fail to build due to missing packages, install them manually.


## Integration Test Checklist

1. Run `docker-compose up --build`.
2. Complete the WordPress installation at `http://localhost:8080`.
3. Activate the **BottomLine AB Tests** plugin and confirm the admin notice appears.
4. Visit the automatically created "A/B Test Sample Page" and ensure the CTA text changes across incognito sessions (variants A/B/C).
5. Click the CTA as different visitors and verify events appear via `GET http://localhost:8000/results/cta_test`.
6. Disable tracking in plugin settings and confirm the original CTA text is restored and no new events are recorded.
7. Access `/dashboard/cta_test` in the React app to monitor live results and use **Apply Winning Variant** to save the leading variant.
