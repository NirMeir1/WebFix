#!/bin/bash
# Setup script for BottomLine WordPress A/B testing environment
# This script starts WordPress via docker-compose, installs the plugin,
# and runs backend/frontend tests.

set -euo pipefail

# Ensure docker is available
if ! command -v docker >/dev/null; then
  echo "Docker is required" >&2
  exit 1
fi

# Start WordPress and MySQL containers
if [ ! -f docker-compose.yml ]; then
  echo "docker-compose.yml missing" >&2
  exit 1
fi

docker compose up -d

# Wait for WordPress to finish installing
echo "Waiting for WordPress to initialize..."
sleep 20

# Install WordPress (if not already) and activate plugin
set +e
docker compose exec wordpress wp core install \
  --url="http://localhost:8080" \
  --title="BottomLine" \
  --admin_user="admin" \
  --admin_password="admin" \
  --admin_email="admin@example.com" \
  --skip-email
set -e

docker compose exec wordpress wp plugin activate bottomline-ab-tests

echo "WordPress running at http://localhost:8080 (admin/admin)"

# Setup Python backend and run tests
python3 -m venv venv
source venv/bin/activate
pip install -r ab_tests_backend/requirements.txt
pytest

deactivate

# Run frontend tests
cd frontend
npm install
npx jest --coverage
cd ..

echo "Setup complete."
