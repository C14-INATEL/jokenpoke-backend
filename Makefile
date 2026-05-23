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
# COLORS & STYLES
# =========================================================

GREEN  := $(shell tput setaf 2)
YELLOW := $(shell tput setaf 3)
RED    := $(shell tput setaf 1)
BLUE   := $(shell tput setaf 4)
BOLD   := $(shell tput bold)
NC     := $(shell tput sgr0)

INFO    := $(BLUE)[INFO]$(NC)
SUCCESS := $(GREEN)[SUCCESS]$(NC)
WARNING := $(YELLOW)[WARNING]$(NC)
ERROR   := $(RED)[ERROR]$(NC)

SEPARATOR = =========================================================

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
	@echo ""
	@if $(DC) ps | grep api > /dev/null; then \
		echo "$(SUCCESS) API container is running perfectly!"; \
	else \
		echo "$(ERROR) API container is not running. Run 'make up' first."; \
		exit 1; \
	fi

# =========================================================
# HELP
# =========================================================

help:
	@echo ""
	@echo "$(BOLD)Available commands:$(NC)"
	@echo ""
	@echo "$(BLUE)Local Development:"
	@echo ""
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make install" "Install dependencies locally"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make local-run" "Run API locally with hot reload"
	@echo ""
	@echo ""
	@echo "$(BLUE)Local Testing:$(NC)"
	@echo ""
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make test" "Run all tests locally"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make test-unit" "Run unit tests locally"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make test-integration" "Run integration tests locally"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make watch-test" "Run tests in watch mode"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make watch-unit" "Run unit tests in watch mode"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make watch-integration" "Run integration tests in watch mode"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make test-cov" "Run tests with coverage locally"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make test-ci" "Run CI-style tests locally"
	@echo ""
	@echo ""
	@echo "$(BLUE)Local Code Quality:$(NC)"
	@echo ""
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make format" "Format code locally with Ruff"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make lint" "Run Ruff linter locally"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make lint-fix" "Auto-fix lint issues locally"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make pre-commit" "Run format + lint-fix + tests"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make check" "Run lint + tests locally"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make check-all" "Run full local validation"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make ci" "Run local CI validation pipeline"
	@echo ""
	@echo ""
	@echo "$(BLUE)Docker Development:$(NC)"
	@echo ""
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make dev" "Run API with Docker Compose"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make build" "Build containers"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make up" "Start containers in detached mode"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make down" "Stop containers"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make restart" "Restart containers"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make logs" "Show API logs"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make shell" "Access API container shell"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make clean" "Remove containers and volumes"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make jenkins-rebuild" "Rebuild Jenkins container"
	@echo ""
	@echo ""
	@echo "$(BLUE)Docker Testing:$(NC)"
	@echo ""
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make docker-test" "Run all tests in Docker"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make docker-test-unit" "Run unit tests in Docker"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make docker-test-integration" "Run integration tests in Docker"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make docker-test-cov" "Run tests with coverage in Docker"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make docker-test-ci" "Run CI-style tests in Docker"
	@echo ""
	@echo ""
	@echo "$(BLUE)Docker Code Quality:$(NC)"
	@echo ""
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make docker-format" "Format code in Docker"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make docker-lint" "Run Ruff linter in Docker"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make docker-lint-fix" "Auto-fix lint issues in Docker"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make docker-check" "Run lint + tests in Docker"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make docker-check-all" "Run full Docker validation"
	@echo ""
	@echo ""
	@echo "$(BLUE)Utilities:$(NC)"
	@echo ""
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make env-check" "Validate .env file"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make freeze" "Update poetry.lock locally"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make docker-freeze" "Update poetry.lock in Docker"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make stats" "Show Python code statistics"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make tree" "Show project structure"
	@echo ""
	@echo ""
	@echo "$(BLUE)Cleanup:$(NC)"
	@echo ""
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make clean-cache" "Remove cache and temp files"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make clean-venv" "Remove local virtual environment"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make reset" "Full project reset"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make docker-prune" "Remove unused Docker resources"
	@echo ""
	@echo ""
	@echo "$(BLUE)Shortcuts:$(NC)"
	@echo ""
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make dtest" "Alias for docker-test"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make dlint" "Alias for docker-lint"
	@printf "  $(GREEN)%-30s$(NC) %s\n" "make dformat" "Alias for docker-format"
	@echo ""

# =========================================================
# LOCAL DEVELOPMENT
# =========================================================

install:
	@echo "$(INFO) Installing dependencies..."
	@poetry install
	@echo "$(SUCCESS) Dependencies installed successfully."

local-run:
	@echo "$(INFO) Starting local development server..."
	@$(POETRY) uvicorn $(APP) --host $(HOST) --port $(PORT) --reload

# =========================================================
# DOCKER DEVELOPMENT
# =========================================================

dev:
	@echo "$(INFO) Starting development environment..."
	@echo ""
	@$(DC) up --build

build:
	@echo "$(INFO) Building containers..."
	@echo ""
	@$(DC) build
	@echo ""
	@echo "$(SUCCESS) Containers built successfully."

up:
	@echo "$(INFO) Starting containers..."
	@echo ""
	@$(DC) up -d
	@echo ""
	@echo "$(SUCCESS) Containers started successfully."

down:
	@echo "$(INFO) Stopping containers..."
	@echo ""
	@$(DC) down
	@echo ""
	@echo "$(SUCCESS) Containers stopped successfully."

restart:
	@echo "$(INFO) Restarting containers..."
	@echo ""
	@$(DC) restart
	@echo ""
	@echo "$(SUCCESS) Containers restarted successfully."

logs:
	@echo "$(INFO) Showing API logs..."
	@echo ""
	@$(DC) logs -f api

shell:
	@echo "$(INFO) Accessing API container shell..."
	@echo ""
	@$(DC) exec api bash
	@echo ""
	@echo "$(WARNING) Exiting API container shell..."

clean:
	@echo "$(WARNING) Removing containers and volumes..."
	@echo ""
	@$(DC) down -v --remove-orphans
	@$(MAKE) clean-cache
	@echo ""
	@echo "$(SUCCESS) Docker environment cleaned successfully."

jenkins-rebuild:
	@echo "$(INFO) Rebuilding Jenkins container..."
	@echo ""
	@$(DC) down jenkins
	@$(DC) build --no-cache jenkins
	@$(DC) up -d jenkins
	@echo ""
	@echo "$(SUCCESS) Jenkins container rebuilt successfully."

# =========================================================
# TESTS (LOCAL)
# =========================================================

test:
	@echo "$(INFO) Running all tests locally..."
	@echo ""
	@$(POETRY) $(PYTEST) tests/ -v

test-unit:
	@echo "$(INFO) Running unit tests locally..."
	@echo ""
	@$(POETRY) $(PYTEST) tests/unit -v

test-integration:
	@echo "$(INFO) Running integration tests locally..."
	@echo ""
	@$(POETRY) $(PYTEST) tests/integration -v

watch-test:
	@echo "$(INFO) Running tests in watch mode..."
	@echo ""
	@$(POETRY) ptw \
		--ignore .venv \
		--ignore htmlcov \
		--ignore .pytest_cache

watch-unit:
	@echo "$(INFO) Running unit tests in watch mode..."
	@echo ""
	@$(POETRY) ptw tests/unit

watch-integration:
	@echo "$(INFO) Running integration tests in watch mode..."
	@echo ""
	@$(POETRY) ptw tests/integration

test-cov:
	@echo "$(INFO) Running tests with coverage..."
	@echo ""
	@$(POETRY) $(PYTEST) tests/ \
		--cov=app \
		--cov-report=term-missing \
		--cov-report=html

test-ci:
	@echo "$(INFO) Running CI-style tests locally..."
	@echo ""
	@$(POETRY) $(PYTEST) tests/ \
		--junitxml=reports/test-results.xml \
		--cov=app \
		--cov-report=xml:reports/coverage.xml \
		--cov-report=html:reports/coverage-html \
		--cov-report=term-missing

# =========================================================
# TESTS (DOCKER)
# =========================================================

docker-test: ensure-up
	@echo "$(INFO) Running all tests in Docker..."
	@echo ""
	@$(DOCKER_RUN) $(PYTEST) tests/ -v

docker-test-unit: ensure-up
	@echo "$(INFO) Running unit tests in Docker..."
	@echo ""
	@$(DOCKER_RUN) $(PYTEST) tests/unit -v

docker-test-integration: ensure-up
	@echo "$(INFO) Running integration tests in Docker..."
	@echo ""
	@$(DOCKER_RUN) $(PYTEST) tests/integration -v

docker-test-cov: ensure-up
	@echo "$(INFO) Running tests with coverage in Docker..."
	@echo ""
	@$(DOCKER_RUN) $(PYTEST) tests/ \
		--cov=app \
		--cov-report=term-missing \
		--cov-report=html

docker-test-ci: ensure-up
	@echo "$(INFO) Running CI-style tests in Docker..."
	@echo ""
	@$(DOCKER_RUN) $(PYTEST) tests/ \
		--junitxml=reports/test-results.xml \
		--cov=app \
		--cov-report=xml:reports/coverage.xml \
		--cov-report=html:reports/coverage-html \
		--cov-report=term-missing

# =========================================================
# CODE QUALITY (LOCAL)
# =========================================================

format:
	@echo "$(INFO) Formatting code locally..."
	@echo ""
	@$(POETRY) ruff format .

lint:
	@echo "$(INFO) Running Ruff linter locally..."
	@echo ""
	@$(POETRY) ruff check .

lint-fix:
	@echo "$(INFO) Fixing lint issues locally..."
	@echo ""
	@$(POETRY) ruff check . --fix

pre-commit:
	@echo "$(INFO) Running pre-commit pipeline..."
	@echo ""
	@$(MAKE) format
	@$(MAKE) lint-fix
	@$(MAKE) test
	@echo ""
	@echo "$(SUCCESS) Pre-commit pipeline completed."

check:
	@echo "$(INFO) Running local checks..."
	@echo ""
	@$(MAKE) lint
	@$(MAKE) test
	@echo ""
	@echo "$(SUCCESS) Local checks completed."

check-all:
	@echo "$(INFO) Running full local validation..."
	@echo ""
	@$(MAKE) env-check
	@$(MAKE) format
	@$(MAKE) lint
	@$(MAKE) test-cov
	@echo ""
	@echo "$(SUCCESS) Full local validation completed."

ci:
	@echo "$(INFO) Running local CI pipeline..."
	@echo ""
	@$(MAKE) lint
	@$(MAKE) test-ci
	@echo ""
	@echo "$(SUCCESS) Local CI pipeline completed."

# =========================================================
# CODE QUALITY (DOCKER)
# =========================================================

docker-format: ensure-up
	@echo "$(INFO) Formatting code in Docker..."
	@echo ""
	@$(DOCKER_RUN) ruff format .

docker-lint: ensure-up
	@echo "$(INFO) Running Ruff linter in Docker..."
	@echo ""
	@$(DOCKER_RUN) ruff check .

docker-lint-fix: ensure-up
	@echo "$(INFO) Fixing lint issues in Docker..."
	@echo ""
	@$(DOCKER_RUN) ruff check . --fix

docker-check:
	@echo "$(INFO) Running Docker checks..."
	@echo ""
	@$(MAKE) docker-lint
	@$(MAKE) docker-test
	@echo ""
	@echo "$(SUCCESS) Docker checks completed."

docker-check-all:
	@echo "$(INFO) Running full Docker validation..."
	@echo ""
	@$(MAKE) env-check
	@$(MAKE) docker-format
	@$(MAKE) docker-lint
	@$(MAKE) docker-test-cov
	@echo ""
	@echo "$(SUCCESS) Full Docker validation completed."

# =========================================================
# UTILITIES
# =========================================================

env-check:
	@echo "$(INFO) Checking environment variables..."
	@echo ""
	@test -f .env || (echo "$(ERROR) .env file not found!" && exit 1)
	@echo ""
	@echo "$(SUCCESS) Environment variables validated."

freeze:
	@echo "$(INFO) Updating poetry.lock locally..."
	@echo ""
	@poetry lock
	@echo ""
	@echo "$(SUCCESS) poetry.lock updated successfully."

docker-freeze: ensure-up
	@echo "$(INFO) Updating poetry.lock in Docker..."
	@echo ""
	@$(DOCKER_RUN) poetry lock
	@echo ""
	@echo "$(SUCCESS) poetry.lock updated successfully in Docker."

stats:
	@echo "$(INFO) Showing Python code statistics..."
	@echo ""
	@find app tests -name "*.py" | xargs wc -l

tree:
	@echo "$(INFO) Showing project structure..."
	@echo ""
	@tree -I "__pycache__|.pytest_cache|.ruff_cache|.venv"

# =========================================================
# CLEANUP
# =========================================================

clean-cache:
	@echo ""
	@echo "$(WARNING) Removing cache and temporary files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@find . -type d -name ".ruff_cache" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@rm -rf .coverage htmlcov reports
	@echo "$(SUCCESS) Cache and temporary files removed."

clean-venv:
	@echo "$(WARNING) Removing local virtual environment..."
	@echo ""
	@rm -rf .venv
	@echo ""
	@echo "$(SUCCESS) Virtual environment removed."

reset:
	@echo "$(WARNING) Running full project reset..."
	@echo ""
	@$(MAKE) clean
	@$(MAKE) clean-cache
	@$(MAKE) clean-venv
	@echo ""
	@echo "$(SUCCESS) Project reset completed."

docker-prune:
	@echo "$(WARNING) Removing unused Docker resources..."
	@echo ""
	@docker system prune -af
	@echo ""
	@echo "$(SUCCESS) Unused Docker resources removed."

# =========================================================
# SHORTCUTS
# =========================================================

dtest: docker-test

dlint: docker-lint

dformat: docker-format