# =========================================================
# PHONY
# =========================================================

.PHONY: help install local-run dev test test-unit \
test-integration test-cov test-ci watch-test \
watch-unit watch-integration format lint \
lint-fix pre-commit check check-all ci \
docker-test docker-test-unit docker-test-integration \
docker-test-cov docker-test-ci docker-format \
docker-lint docker-lint-fix docker-check \
docker-check-all build up down restart logs \
shell clean env-check freeze docker-freeze \
stats tree clean-cache clean-venv reset \
docker-prune ensure-up dtest dlint dformat

# =========================================================
# COLORS
# =========================================================

GREEN  = \033[0;32m
YELLOW = \033[1;33m
RED    = \033[0;31m
BLUE   = \033[0;34m
NC     = \033[0m

# =========================================================
# VARIABLES
# =========================================================

APP = app.main:app
HOST = 0.0.0.0
PORT = 8000

PYTEST = pytest --tb=short -s

DC = docker compose

POETRY = poetry run
DOCKER_RUN = $(DC) exec api poetry run

# =========================================================
# HELPERS
# =========================================================

ensure-up:
	@$(DC) ps | grep api > /dev/null || \
	(echo "API container is not running. Run 'make up' first." && exit 1)

# =========================================================
# HELP
# =========================================================

help:
	@echo ""
	@echo "Available commands:"
	@echo ""
	@echo "Local Development:"
	@echo "  make install              		Install dependencies locally"
	@echo "  make local-run            		Run API locally with hot reload"
	@echo ""
	@echo "Local Testing:"
	@echo "  make test                 		Run all tests locally"
	@echo "  make test-unit            		Run unit tests locally"
	@echo "  make test-integration     		Run integration tests locally"
	@echo "  make watch-test           		Run tests in watch mode"
	@echo "  make watch-unit           		Run unit tests in watch mode"
	@echo "  make watch-integration    		Run integration tests in watch mode"
	@echo "  make test-cov             		Run tests with coverage locally"
	@echo "  make test-ci              		Run CI-style tests locally"
	@echo ""
	@echo "Local Code Quality:"
	@echo "  make format               		Format code locally with Ruff"
	@echo "  make lint                 		Run Ruff linter locally"
	@echo "  make lint-fix             		Auto-fix lint issues locally"
	@echo "  make pre-commit           		Run format + lint-fix + tests"
	@echo "  make check                		Run lint + tests locally"
	@echo "  make check-all            		Run full local validation"
	@echo "  make ci                   		Run local CI validation pipeline"
	@echo ""
	@echo "Docker Development:"
	@echo "  make dev                  		Run API with Docker Compose"
	@echo "  make build                		Build containers"
	@echo "  make up                   		Start containers in detached mode"
	@echo "  make down                 		Stop containers"
	@echo "  make restart              		Restart containers"
	@echo "  make logs                 		Show API logs"
	@echo "  make shell                		Access API container shell"
	@echo "  make clean                		Remove containers and volumes"
	@echo "  make jenkins-rebuild      		Rebuild Jenkins container"
	@echo ""
	@echo "Docker Testing:"
	@echo "  make docker-test          		Run all tests in Docker"
	@echo "  make docker-test-unit     		Run unit tests in Docker"
	@echo "  make docker-test-integration	Run integration tests in Docker"
	@echo "  make docker-test-cov      		Run tests with coverage in Docker"
	@echo "  make docker-test-ci       		Run CI-style tests in Docker"
	@echo ""
	@echo "Docker Code Quality:"
	@echo "  make docker-format        		Format code in Docker"
	@echo "  make docker-lint          		Run Ruff linter in Docker"
	@echo "  make docker-lint-fix      		Auto-fix lint issues in Docker"
	@echo "  make docker-check         		Run lint + tests in Docker"
	@echo "  make docker-check-all     		Run full Docker validation"
	@echo ""
	@echo "Utilities:"
	@echo "  make env-check            		Validate .env file"
	@echo "  make freeze               		Update poetry.lock locally"
	@echo "  make docker-freeze        		Update poetry.lock in Docker"
	@echo "  make stats                		Show Python code statistics"
	@echo "  make tree                 		Show project structure"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean-cache          		Remove cache and temp files"
	@echo "  make clean-venv           		Remove local virtual environment"
	@echo "  make reset                		Full project reset"
	@echo "  make docker-prune         		Remove unused Docker resources"
	@echo ""
	@echo "Shortcuts:"
	@echo "  make dtest                		Alias for docker-test"
	@echo "  make dlint                		Alias for docker-lint"
	@echo "  make dformat              		Alias for docker-format"
	@echo ""

# =========================================================
# LOCAL DEVELOPMENT
# =========================================================

install:
	@echo "$(BLUE)Installing dependencies...$(NC)"
	@poetry install
	@echo "$(GREEN)Dependencies installed successfully!$(NC)"

local-run:
	$(POETRY) uvicorn $(APP) --host $(HOST) --port $(PORT) --reload

# =========================================================
# DOCKER DEVELOPMENT
# =========================================================

dev:
	$(DC) up --build

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

jenkins-rebuild:
	$(DC) down jenkins
	$(DC) build --no-cache jenkins
	$(DC) up -d jenkins

# =========================================================
# TESTS (LOCAL)
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
# TESTS (DOCKER)
# =========================================================

docker-test: ensure-up
	$(DOCKER_RUN) $(PYTEST) tests/ -v

docker-test-unit: ensure-up
	$(DOCKER_RUN) $(PYTEST) tests/unit -v

docker-test-integration: ensure-up
	$(DOCKER_RUN) $(PYTEST) tests/integration -v

docker-test-cov: ensure-up
	$(DOCKER_RUN) $(PYTEST) tests/ \
		--cov=app \
		--cov-report=term-missing \
		--cov-report=html

docker-test-ci: ensure-up
	$(DOCKER_RUN) $(PYTEST) tests/ \
		--junitxml=reports/test-results.xml \
		--cov=app \
		--cov-report=xml:reports/coverage.xml \
		--cov-report=html:reports/coverage-html \
		--cov-report=term-missing

# =========================================================
# CODE QUALITY (LOCAL)
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
# CODE QUALITY (DOCKER)
# =========================================================

docker-format: ensure-up
	$(DOCKER_RUN) ruff format .

docker-lint: ensure-up
	$(DOCKER_RUN) ruff check .

docker-lint-fix: ensure-up
	$(DOCKER_RUN) ruff check . --fix

docker-check:
	$(MAKE) docker-lint
	$(MAKE) docker-test

docker-check-all:
	$(MAKE) env-check
	$(MAKE) docker-format
	$(MAKE) docker-lint
	$(MAKE) docker-test-cov

# =========================================================
# UTILITIES
# =========================================================

env-check:
	@echo "Checking environment variables..."
	@test -f .env || (echo ".env file not found!" && exit 1)

freeze:
	poetry lock

docker-freeze: ensure-up
	$(DOCKER_RUN) poetry lock

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

# =========================================================
# SHORTCUTS
# =========================================================

dtest: docker-test

dlint: docker-lint

dformat: docker-format