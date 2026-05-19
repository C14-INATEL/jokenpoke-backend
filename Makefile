# =========================================================
# PHONY
# =========================================================

.PHONY: help install local-run dev test test-unit \
test-integration test-cov test-ci format lint \
lint-fix check build up down restart logs \
shell clean env-check freeze tree ci

# =========================================================
# VARIABLES
# =========================================================

APP = app.main:app
HOST = 0.0.0.0
PORT = 8000

PYTEST = pytest --tb=short -s
DC = docker compose
POETRY = poetry run

# =========================================================
# HELP
# =========================================================

help:
	@echo ""
	@echo "Available commands:"
	@echo ""
	@echo "Development:"
	@echo "  make install              Install dependencies"
	@echo "  make local-run            Run API locally"
	@echo "  make dev                  Run API with Docker"
	@echo ""
	@echo "Testing:"
	@echo "  make test                 Run all tests"
	@echo "  make test-unit            Run unit tests"
	@echo "  make test-integration     Run integration tests"
	@echo "  make test-cov             Run tests with coverage"
	@echo "  make test-ci              Run CI-style tests"
	@echo ""
	@echo "Code Quality:"
	@echo "  make format               Format code"
	@echo "  make lint                 Run linter"
	@echo "  make lint-fix             Auto-fix lint issues"
	@echo "  make check                Run lint + tests"
	@echo "  make ci                   Full CI validation"
	@echo ""
	@echo "Docker:"
	@echo "  make build                Build containers"
	@echo "  make up                   Start containers"
	@echo "  make down                 Stop containers"
	@echo "  make restart              Restart containers"
	@echo "  make logs                 Show API logs"
	@echo "  make shell                Access API container"
	@echo "  make clean                Remove containers/volumes"
	@echo ""
	@echo "Utilities:"
	@echo "  make env-check            Validate .env file"
	@echo "  make freeze               Update poetry.lock"
	@echo "  make tree                 Show project structure"
	@echo ""

# =========================================================
# INSTALL
# =========================================================

install:
	poetry install

# =========================================================
# LOCAL DEVELOPMENT
# =========================================================

local-run:
	$(POETRY) uvicorn $(APP) --host $(HOST) --port $(PORT) --reload

dev:
	$(DC) up --build

# =========================================================
# TESTS
# =========================================================

test:
	$(POETRY) $(PYTEST) tests/ -v

test-unit:
	$(POETRY) $(PYTEST) tests/unit -v

test-integration:
	$(POETRY) $(PYTEST) tests/integration -v

test-cov:
	$(POETRY) $(PYTEST) tests/ \
		--cov=app \
		--cov-report=term-missing \
		--cov-report=html

test-ci:
	$(POETRY) $(PYTEST) tests/ \
		--junitxml=reports/test-results.xml \
		--cov=app \
		--cov-report=xml:reports/coverage.xml \
		--cov-report=html:reports/coverage-html \
		--cov-report=term-missing

# =========================================================
# CODE QUALITY
# =========================================================

format:
	$(POETRY) ruff format .

lint:
	$(POETRY) ruff check .

lint-fix:
	$(POETRY) ruff check . --fix

check:
	$(MAKE) lint
	$(MAKE) test

ci:
	$(MAKE) lint
	$(MAKE) test-ci

# =========================================================
# DOCKER
# =========================================================

build:
	$(DC) build

up:
	$(DC) up -d

down:
	$(DC) down

restart:
	$(DC) restart

logs:
	$(DC) logs -f api

shell:
	$(DC) exec api bash

clean:
	$(DC) down -v --remove-orphans

# =========================================================
# UTILITIES
# =========================================================

env-check:
	@echo "Checking environment variables..."
	@test -f .env || (echo ".env file not found!" && exit 1)

freeze:
	poetry lock

tree:
	tree -I "__pycache__|.pytest_cache|.ruff_cache|.venv"
