#!/bin/sh
set -e
echo "Applying database migrations..."
alembic upgrade head
echo "Seeding baseline data if needed..."
python -m app.seed
echo "Starting server..."
exec uvicorn app.server:app --host 0.0.0.0 --port 8000 --workers 4