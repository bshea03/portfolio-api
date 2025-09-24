#!/bin/bash
# wait-for-postgres.sh
set -e

host="$1"
user="$2"
shift 2
cmd="$@"

# fallback to env var or postgres if not provided
user="${user:-${POSTGRES_USER:-postgres}}"

# Configurable retry limit and delay
MAX_RETRIES=${MAX_RETRIES:-30}
RETRY_INTERVAL=${RETRY_INTERVAL:-2}
COUNT=0

echo "Waiting for PostgreSQL at $host:5432 as user '$user'..."

until pg_isready -h "$host" -p 5432 -U "$user" >/dev/null 2>&1; do
  COUNT=$((COUNT + 1))
  if [ "$COUNT" -ge "$MAX_RETRIES" ]; then
    echo "❌ PostgreSQL not ready after $((MAX_RETRIES * RETRY_INTERVAL)) seconds. Exiting."
    exit 1
  fi
  echo "⏳ Attempt $COUNT/$MAX_RETRIES: PostgreSQL not ready yet..."
  sleep $RETRY_INTERVAL
done

echo "✅ PostgreSQL is ready. Running command: $cmd"
exec "$cmd"
