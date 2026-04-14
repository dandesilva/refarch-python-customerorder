.PHONY: help build up down logs shell test clean migrate

# Use podman-compose by default
COMPOSE = podman-compose

help:
	@echo "Customer Order Services - Python Edition"
	@echo ""
	@echo "Available commands:"
	@echo "  make build    - Build container images"
	@echo "  make up       - Start all services"
	@echo "  make down     - Stop all services"
	@echo "  make logs     - View logs"
	@echo "  make shell    - Open shell in app container"
	@echo "  make migrate  - Run database migrations"
	@echo "  make test     - Run tests"
	@echo "  make clean    - Clean up containers and volumes"

build:
	$(COMPOSE) build

up:
	$(COMPOSE) up -d
	@echo "Application starting..."
	@echo "API will be available at http://localhost:8000"
	@echo "API docs at http://localhost:8000/api/docs"

down:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f

shell:
	$(COMPOSE) exec app /bin/bash

migrate:
	$(COMPOSE) exec app alembic upgrade head

test:
	$(COMPOSE) exec app pytest

clean:
	$(COMPOSE) down -v
	podman system prune -f
