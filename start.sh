#!/bin/bash
set -e

echo "🌍 Environment: ${APP_ENV:-dev}"

if [ "$APP_ENV" = "dev" ]; then
  echo "📦 Running Alembic migrations (dev)..."
  alembic upgrade head
else
  echo "⚠️ Skipping Alembic migrations (prod)..."
fi

echo "🚀 Starting FastAPI app..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --log-level info
