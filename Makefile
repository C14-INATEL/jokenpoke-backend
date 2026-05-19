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

# =========================================================
# HELP
# =========================================================

help:
	@echo ""
	@echo "Available commands:"
	@echo ""
	@echo "Development:"
	@echo "  make install              Install dependencies"
	@echo "  make local-run            Run API locally with hot reload"
	@echo "  make dev                  Run API with Docker Compose"
	@echo ""
	@echo "Testing:"
	@echo "  make test                 Run all tests"
	@echo "  make test-unit            Run unit tests"
	@echo "  make test-integration     Run integration tests"
	@echo "  make watch-test           Run tests in watch mode"
	@echo "  make watch-unit           Run unit tests in watch mode"
	@echo "  make watch-integration    Run integration tests in watch mode"
	@echo "  make test-cov             Run tests with coverage report"
	@echo "  make test-ci              Run CI-style tests with reports"
	@echo ""
	@echo "Code Quality:"
	@echo "  make format               Format code with Ruff"
	@echo "  make lint                 Run Ruff linter"
	@echo "  make lint-fix             Auto-fix lint issues"
	@echo "  make pre-commit           Run format + lint-fix + tests"
	@echo "  make check                Run lint + tests"
	@echo "  make check-all            Run full local validation"
	@echo "  make ci                   Run CI validation pipeline"
	@echo ""
	@echo "Docker:"
	@echo "  make build                Build containers"
	@echo "  make up                   Start containers in detached mode"
	@echo "  make down                 Stop containers"
	@echo "  make restart              Restart containers"
	@echo "  make logs                 Show API logs"
	@echo "  make shell                Access API container shell"
	@echo "  make clean                Remove containers and volumes"
	@echo "  make docker-prune         Remove unused Docker resources"
	@echo ""
	@echo "Utilities:"
	@echo "  make env-check            Validate .env file"
	@echo "  make freeze               Update poetry.lock"
	@echo "  make stats                Show Python code statistics"
	@echo "  make tree                 Show project structure"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean-cache          Remove cache and temporary files"
	@echo "  make clean-venv           Remove virtual environment"
	@echo "  make reset                Full project reset"
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

watch-test:
	$(POETRY) ptw \
		--ignore .venv \
		--ignore htmlcov \
		--ignore .pytest_cache

watch-unit:
	$(POETRY) ptw tests/unit

watch-integration:
	$(POETRY) ptw tests/integration

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

pre-commit:
	$(MAKE) format
	$(MAKE) lint-fix
	$(MAKE) test

check:
	$(MAKE) lint
	$(MAKE) test

check-all:
	$(MAKE) env-check
	$(MAKE) format
	$(MAKE) lint
	$(MAKE) test-cov

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
	$(MAKE) clean-cache

# =========================================================
# UTILITIES
# =========================================================

env-check:
	@echo "Checking environment variables..."
	@test -f .env || (echo ".env file not found!" && exit 1)

freeze:
	poetry lock

stats:
	find app tests -name "*.py" | xargs wc -l

tree:
	tree -I "__pycache__|.pytest_cache|.ruff_cache|.venv"

# =========================================================
# CLEANUP
# =========================================================

clean-cache:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .coverage htmlcov reports

clean-venv:
	rm -rf .venv

reset:
	$(MAKE) clean
	$(MAKE) clean-cache
	$(MAKE) clean-venv

docker-prune:
	docker system prune -af
