FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Install PostgreSQL client tools for pg_isready
RUN apt-get update && apt-get install -y postgresql-client curl certbot python3-certbot-nginx

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Add wait-for-postgres script
COPY wait-for-postgres.sh /wait-for-postgres.sh
RUN chmod +x /wait-for-postgres.sh

# Add startup script to run Alembic + Uvicorn
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Wait for DB, then run migrations + start FastAPI
CMD ["bash", "-c", "pg_isready -h db -U ${POSTGRES_USER:-postgres} && /wait-for-postgres.sh db ${POSTGRES_USER:-postgres} /start.sh"]
