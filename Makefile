# Makefile for FastAPI + PostgreSQL Docker setup (Docker CLI v2)

.PHONY: up down restart migrate revision current psql logs bash dbshell clean test backup restore doctor compose-env


env ?= dev
ENV_FILE := .env.$(env)

compose-env:
	@cp .env.$(env) .env
	@echo "" >> .env
	@echo "APP_ENV=$(env)" >> .env
	@echo "ENV_FILE=.env.$(env)" >> .env

up: compose-env
	docker compose up -d --build

down:
	docker compose down

restart:
	docker compose down && docker compose up -d --build

migrate:
	docker compose exec api alembic upgrade head

revision:
	docker compose exec api alembic revision --autogenerate -m "$(m)"
	
current:
	docker compose exec api alembic current

psql:
	docker compose exec db psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)

logs:
	docker compose logs -f

bash:
	docker compose exec api bash

dbshell:
	docker compose exec db bash

clean:
	docker compose down -v --remove-orphans

backup:
	docker compose exec db pg_dump -U $(POSTGRES_USER) -d $(POSTGRES_DB) -F c -f /var/lib/postgresql/data/backup.dump
	@echo "✅ Backup saved to Docker volume (pgdata). Use 'make dbshell' to retrieve it."

restore:
	docker compose exec db pg_restore -U $(POSTGRES_USER) -d $(POSTGRES_DB) /var/lib/postgresql/data/backup.dump
	@echo "✅ Database restored from backup.dump"
	
doctor:
	@echo "🔍 Checking Docker containers..."
	docker compose ps
	@echo "\n🔍 Checking environment variables..."
	docker compose exec api env | grep DATABASE_URL || echo "❌ DATABASE_URL not found"
	@echo "\n🔍 Checking Alembic metadata..."
	docker compose exec api python -c "from app.database import Base; from app.models import *; print(Base.metadata.tables.keys())"
	@echo "\n🔍 Checking DB health..."
	docker compose exec db bash -c 'pg_isready -U "$$POSTGRES_USER"' || echo "❌ Postgres not ready"
test:
	docker compose run --rm test-runner