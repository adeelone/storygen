.PHONY: install dev build test lint format typecheck migrate seed eval clean

install:
	python -m pip install -e "./backend[dev]"
	cd frontend && npm install

dev:
	docker compose up --build

build:
	docker compose build

test:
	cd backend && pytest
	cd frontend && npm test

lint:
	cd backend && ruff check app tests && black --check app tests
	cd frontend && npm run lint

format:
	cd backend && ruff check --fix app tests && black app tests
	cd frontend && npm run format

typecheck:
	cd backend && mypy app
	cd frontend && npm run typecheck

migrate:
	@echo "Cloud SQL migrations are introduced when SQLAlchemy storage is enabled; local JSON persistence needs no migration."

seed:
	@echo "Generate sample stories through the UI using the deterministic mock providers."

eval:
	cd backend && python -m app.eval

clean:
	@echo "Remove generated .data, reports, coverage, and build folders manually when needed."
