# =========================================================
# PHONY
# =========================================================

.PHONY: help bootstrap install local-run dev \
	test test-unit test-integration test-cov test-cov-strict test-ci \
	watch-test watch-unit watch-integration \
	format format-check lint lint-fix \
	quality pre-commit check check-all ci \
	security security-full \
	docker-test docker-test-unit docker-test-integration \
	docker-test-cov docker-test-ci \
	docker-format docker-lint docker-lint-fix \
	docker-check docker-check-all \
	build up down restart logs shell clean \
	jenkins-rebuild \
	dev-pipeline \
	env-check freeze docker-freeze \
	stats tree \
	clean-cache clean-venv clean-dist reset docker-prune \
	ensure-up notify-test \
	dtest dlint dformat

# =========================================================
# COLORS & STYLES
# =========================================================

GREEN  := $(shell tput setaf 2 2>/dev/null || echo "")
YELLOW := $(shell tput setaf 3 2>/dev/null || echo "")
RED    := $(shell tput setaf 1 2>/dev/null || echo "")
BLUE   := $(shell tput setaf 4 2>/dev/null || echo "")
BOLD   := $(shell tput bold   2>/dev/null || echo "")
NC     := $(shell tput sgr0   2>/dev/null || echo "")

INFO    := $(BLUE)[INFO]$(NC)
SUCCESS := $(GREEN)[SUCCESS]$(NC)
WARNING := $(YELLOW)[WARNING]$(NC)
ERROR   := $(RED)[ERROR]$(NC)

# =========================================================
# VARIABLES
# =========================================================

APP  = app.main:app
HOST = 0.0.0.0
PORT = 8000

# Threshold de cobertura — deve ser igual ao Jenkins (COVERAGE_THRESHOLD=90)
COVERAGE_THRESHOLD := 90

# Flags base do pytest
PYTEST = pytest --tb=short -s

# Flags de cobertura reutilizadas nos targets de CI
PYTEST_COV_FLAGS = \
	--cov=app \
	--cov-report=xml:reports/coverage.xml \
	--cov-report=html:reports/coverage-html \
	--cov-report=term-missing

DC         = docker compose
POETRY     = poetry run
DOCKER_RUN = $(DC) exec api poetry run

# =========================================================
# HELPERS
# =========================================================

# Verifica se o container da API está rodando antes de targets Docker.
ensure-up:
	@if $(DC) ps 2>/dev/null | grep -q api; then \
		echo "$(SUCCESS) API container is running."; \
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
	@echo "$(BLUE)Setup:$(NC)"
	@echo ""
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make bootstrap"        "First-time setup: copy .env, install deps, start containers"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make install"          "Install dependencies locally via Poetry"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make env-check"        "Check that .env file exists"
	@echo ""
	@echo "$(BLUE)Local Development:$(NC)"
	@echo ""
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make local-run"        "Run API locally with hot reload"
	@echo ""
	@echo "$(BLUE)Local Testing:$(NC)"
	@echo ""
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make test"             "Run all tests locally"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make test-unit"        "Run unit tests locally"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make test-integration" "Run integration tests locally"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make test-cov"         "Run tests with coverage report"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make test-cov-strict"  "Run tests with coverage (fails below $(COVERAGE_THRESHOLD)%)"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make test-ci"          "Run CI-style tests (mirrors Jenkins threshold)"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make watch-test"       "Run all tests in watch mode"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make watch-unit"       "Run unit tests in watch mode"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make watch-integration" "Run integration tests in watch mode"
	@echo ""
	@echo "$(BLUE)Local Code Quality:$(NC)"
	@echo ""
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make format"           "Format code with Ruff"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make format-check"     "Check formatting without applying changes"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make lint"             "Run Ruff linter"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make lint-fix"         "Auto-fix lint issues with Ruff"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make quality"          "Run lint + format-check + MyPy"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make pre-commit"       "Run format + lint-fix + tests (pre-commit gate)"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make check"            "Run lint + tests"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make check-all"        "Run full local validation (env + format + lint + test-cov)"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make ci"               "Simulate dev-ci pipeline (lint + format-check + test-ci)"
	@echo ""
	@echo "$(BLUE)Security:$(NC)"
	@echo ""
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make security"         "Run pip-audit (dependency CVEs)"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make security-full"    "Run pip-audit + bandit + detect-secrets (mirrors Jenkins)"
	@echo ""
	@echo "$(BLUE)Docker Development:$(NC)"
	@echo ""
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make dev"              "Start full environment with Docker Compose (attached)"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make build"            "Build containers"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make up"               "Start containers in detached mode"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make down"             "Stop containers"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make restart"          "Restart containers"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make logs"             "Stream API logs"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make shell"            "Open shell inside the API container"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make clean"            "Remove containers, volumes and caches"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make jenkins-rebuild"  "Rebuild Jenkins container from scratch"
	@echo ""
	@echo "$(BLUE)Docker Testing:$(NC)"
	@echo ""
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make docker-test"             "Run all tests in Docker"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make docker-test-unit"        "Run unit tests in Docker"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make docker-test-integration" "Run integration tests in Docker"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make docker-test-cov"         "Run tests with coverage in Docker"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make docker-test-ci"          "Run CI-style tests in Docker (threshold: $(COVERAGE_THRESHOLD)%)"
	@echo ""
	@echo "$(BLUE)Docker Code Quality:$(NC)"
	@echo ""
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make docker-format"    "Format code in Docker"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make docker-lint"      "Run Ruff linter in Docker"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make docker-lint-fix"  "Auto-fix lint issues in Docker"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make docker-check"     "Run lint + tests in Docker"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make docker-check-all" "Run full validation in Docker"
	@echo ""
	@echo "$(BLUE)Utilities:$(NC)"
	@echo ""
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make freeze"           "Update poetry.lock locally"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make docker-freeze"    "Update poetry.lock inside Docker container"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make stats"            "Show Python code line counts"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make tree"             "Show project directory structure"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make notify-test"      "Test notification script locally (scripts/notify.py)"
	@echo ""
	@echo "$(BLUE)Cleanup:$(NC)"
	@echo ""
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make clean-cache"      "Remove caches and temporary files"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make clean-venv"       "Remove local virtual environment"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make clean-dist"       "Remove dist/ artifacts"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make reset"            "Full project reset (containers + caches + venv + dist)"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make docker-prune"     "Remove ALL unused Docker resources (destructive)"
	@echo ""
	@echo "$(BLUE)Shortcuts:$(NC)"
	@echo ""
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make dtest"            "Alias: docker-test"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make dlint"            "Alias: docker-lint"
	@printf "  $(GREEN)%-32s$(NC) %s\n" "make dformat"          "Alias: docker-format"
	@echo ""

# =========================================================
# SETUP
# =========================================================

# Configura o ambiente do zero para um novo desenvolvedor.
# Copia .env.example (sem sobrescrever), instala dependências e sobe os containers.
bootstrap:
	@echo "$(INFO) Bootstrapping project..."
	@cp -n .env.example .env 2>/dev/null && \
		echo "$(SUCCESS) .env created from .env.example." || \
		echo "$(WARNING) .env already exists — skipping copy."
	@$(MAKE) install
	@$(MAKE) up
	@echo ""
	@echo "$(SUCCESS) Bootstrap complete. Run 'make help' to see available commands."

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
	@echo "$(INFO) Starting development environment (attached)..."
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
	@echo "$(INFO) Streaming API logs (Ctrl+C to stop)..."
	@echo ""
	@$(DC) logs -f api

shell:
	@echo "$(INFO) Opening shell in API container..."
	@echo ""
	@$(DC) exec api bash
	@echo ""
	@echo "$(WARNING) Exited API container shell."

clean:
	@echo "$(WARNING) Removing containers and volumes..."
	@echo ""
	@$(DC) down -v --remove-orphans
	@$(MAKE) clean-cache
	@echo ""
	@echo "$(SUCCESS) Docker environment cleaned successfully."

# Reconstrói o container Jenkins do zero, útil após atualizar Dockerfile.jenkins.
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

# Executa testes em modo watch — re-roda automaticamente ao salvar arquivos.
watch-test:
	@echo "$(INFO) Running tests in watch mode (Ctrl+C to stop)..."
	@echo ""
	@$(POETRY) ptw . --now

watch-unit:
	@echo "$(INFO) Running unit tests in watch mode..."
	@echo ""
	@$(POETRY) ptw tests/unit --now

watch-integration:
	@echo "$(INFO) Running integration tests in watch mode..."
	@echo ""
	@$(POETRY) ptw tests/integration --now

# Cobertura sem threshold — útil para inspecionar relatórios durante desenvolvimento.
test-cov:
	@echo "$(INFO) Running tests with coverage report..."
	@echo ""
	@mkdir -p reports
	@$(POETRY) $(PYTEST) tests/ \
		--cov=app \
		--cov-report=term-missing \
		--cov-report=html:reports/coverage-html

# Cobertura com threshold — espelha o critério de qualidade do Jenkins.
# Falha se cobertura estiver abaixo de $(COVERAGE_THRESHOLD)%.
test-cov-strict:
	@echo "$(INFO) Running tests with strict coverage (threshold: $(COVERAGE_THRESHOLD)%)..."
	@echo ""
	@mkdir -p reports
	@$(POETRY) $(PYTEST) tests/ \
		--cov=app \
		--cov-report=term-missing \
		--cov-fail-under=$(COVERAGE_THRESHOLD)

# Simula a pipeline de CI localmente com relatórios e threshold.
# Equivalente ao stage 'Unit Tests' + 'Integration Test' do Jenkins.
test-ci:
	@echo "$(INFO) Running CI-style tests locally (threshold: $(COVERAGE_THRESHOLD)%)..."
	@echo ""
	@mkdir -p reports
	@$(POETRY) $(PYTEST) tests/ \
		--tb=short \
		--junitxml=reports/test-results.xml \
		$(PYTEST_COV_FLAGS) \
		--cov-fail-under=$(COVERAGE_THRESHOLD)

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
		--cov-report=html:reports/coverage-html

docker-test-ci: ensure-up
	@echo "$(INFO) Running CI-style tests in Docker (threshold: $(COVERAGE_THRESHOLD)%)..."
	@echo ""
	@$(DOCKER_RUN) $(PYTEST) tests/ \
		--tb=short \
		--junitxml=reports/test-results.xml \
		$(PYTEST_COV_FLAGS) \
		--cov-fail-under=$(COVERAGE_THRESHOLD)

# =========================================================
# CODE QUALITY (LOCAL)
# =========================================================

format:
	@echo "$(INFO) Formatting code with Ruff..."
	@echo ""
	@$(POETRY) ruff format .

# Verifica formatação sem aplicar alterações — usado em CI.
format-check:
	@echo "$(INFO) Checking code formatting..."
	@echo ""
	@$(POETRY) ruff format . --check

lint:
	@echo "$(INFO) Running Ruff linter..."
	@echo ""
	@$(POETRY) ruff check .

lint-fix:
	@echo "$(INFO) Auto-fixing lint issues with Ruff..."
	@echo ""
	@$(POETRY) ruff check . --fix

# Lint + format-check + MyPy. Continue-on-error no MyPy (espelha Actions).
quality:
	@echo "$(INFO) Running code quality checks..."
	@echo ""
	@$(MAKE) lint
	@$(MAKE) format-check
	@echo "$(INFO) Running MyPy static analysis..."
	@$(POETRY) mypy app/ --ignore-missing-imports || \
		echo "$(WARNING) MyPy found typing issues."

# Gate de pré-commit: formata, corrige lint e executa testes.
pre-commit:
	@echo "$(INFO) Running pre-commit gate..."
	@echo ""
	@$(MAKE) format
	@$(MAKE) lint-fix
	@$(MAKE) test
	@echo ""
	@echo "$(SUCCESS) Pre-commit gate passed."

check:
	@echo "$(INFO) Running lint + tests..."
	@echo ""
	@$(MAKE) lint
	@$(MAKE) test
	@echo ""
	@echo "$(SUCCESS) Checks passed."

check-all:
	@echo "$(INFO) Running full local validation..."
	@echo ""
	@$(MAKE) env-check
	@$(MAKE) format
	@$(MAKE) lint
	@$(MAKE) test-cov
	@echo ""
	@echo "$(SUCCESS) Full local validation completed."

# Simula o workflow dev-ci.yml do GitHub Actions:
# lint → format-check → test-ci (com threshold).
ci:
	@echo "$(INFO) Simulating dev-ci pipeline locally..."
	@echo ""
	@$(MAKE) lint
	@$(MAKE) format-check
	@$(MAKE) test-ci
	@echo ""
	@echo "$(SUCCESS) dev-ci pipeline simulation completed."

# Pipeline completo de desenvolvimento — inclui MyPy, security e Docker build.
# Use antes de abrir PR para main.
dev-pipeline:
	@echo "$(INFO) Running full development pipeline..."
	@echo ""
	@$(MAKE) quality
	@$(MAKE) security
	@$(MAKE) test-ci
	@echo "$(INFO) Validating Docker build..."
	@$(DC) build
	@echo ""
	@echo "$(SUCCESS) Development pipeline completed."

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
	@echo "$(INFO) Auto-fixing lint issues in Docker..."
	@echo ""
	@$(DOCKER_RUN) ruff check . --fix

docker-check:
	@echo "$(INFO) Running lint + tests in Docker..."
	@echo ""
	@$(MAKE) docker-lint
	@$(MAKE) docker-test
	@echo ""
	@echo "$(SUCCESS) Docker checks passed."

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
# SECURITY
# =========================================================

# Varredura rápida de dependências (CVEs conhecidos via pip-audit).
security:
	@echo "$(INFO) Running dependency vulnerability scan (pip-audit)..."
	@$(POETRY) pip-audit || \
		echo "$(WARNING) Vulnerabilities detected — review output above."

# Varredura completa — espelha o stage 'Security Scan' do Jenkins:
#   pip-audit  → CVEs em dependências Python
#   bandit     → SAST (análise estática de segurança no código)
#   detect-secrets → secrets e credenciais expostas no código
security-full:
	@echo "$(INFO) Running full security scan (mirrors Jenkins Security Scan stage)..."
	@echo ""
	@echo "$(INFO) [1/3] pip-audit — dependency CVEs..."
	@$(POETRY) pip-audit || \
		echo "$(WARNING) Vulnerabilities detected."
	@echo ""
	@echo "$(INFO) [2/3] bandit — SAST..."
	@$(POETRY) bandit -r app/ \
		--severity-level medium \
		--confidence-level medium || \
		echo "$(WARNING) Bandit found security issues."
	@echo ""
	@echo "$(INFO) [3/3] detect-secrets — exposed credentials..."
	@$(POETRY) detect-secrets scan --baseline .secrets.baseline || \
		echo "$(WARNING) detect-secrets found potential secrets."
	@echo ""
	@echo "$(SUCCESS) Full security scan completed."

# =========================================================
# UTILITIES
# =========================================================

env-check:
	@echo "$(INFO) Checking .env file..."
	@echo ""
	@test -f .env || (echo "$(ERROR) .env file not found. Run: cp .env.example .env" && exit 1)
	@echo "$(SUCCESS) .env file found."

freeze:
	@echo "$(INFO) Updating poetry.lock locally..."
	@echo ""
	@poetry lock
	@echo ""
	@echo "$(SUCCESS) poetry.lock updated."

# CORREÇÃO: poetry lock não é executado via 'poetry run' — usa exec direto no container.
docker-freeze: ensure-up
	@echo "$(INFO) Updating poetry.lock in Docker container..."
	@echo ""
	@$(DC) exec api poetry lock
	@echo ""
	@echo "$(SUCCESS) poetry.lock updated in Docker."

stats:
	@echo "$(INFO) Python code line counts..."
	@echo ""
	@find app tests -name "*.py" | xargs wc -l

# Exibe a árvore do projeto. Requer 'tree' instalado (brew install tree / apt install tree).
tree:
	@echo "$(INFO) Project structure..."
	@echo ""
	@if command -v tree > /dev/null 2>&1; then \
		tree -I "__pycache__|.pytest_cache|.ruff_cache|.venv"; \
	else \
		echo "$(WARNING) 'tree' not found. Falling back to find:"; \
		find . -not \( -path "./.git/*" -o -path "./.venv/*" -o -path "./__pycache__/*" \) | sort; \
	fi

# Testa o script de notificação localmente.
# Útil para validar integrações de email antes de executar a pipeline Jenkins.
notify-test:
	@echo "$(INFO) Testing notification script (scripts/notify.py)..."
	@echo ""
	@python3 scripts/notify.py SUCCESS

# =========================================================
# CLEANUP
# =========================================================

clean-cache:
	@echo "$(WARNING) Removing cache and temporary files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@rm -rf .coverage htmlcov reports
	@echo "$(SUCCESS) Cache and temporary files removed."

clean-venv:
	@echo "$(WARNING) Removing local virtual environment (.venv)..."
	@echo ""
	@rm -rf .venv
	@echo ""
	@echo "$(SUCCESS) Virtual environment removed."

# Remove artefatos gerados pelo stage Package do Jenkins (dist/*.tar.gz).
clean-dist:
	@echo "$(WARNING) Removing dist/ artifacts..."
	@rm -rf dist/
	@echo "$(SUCCESS) dist/ removed."

reset:
	@echo "$(WARNING) Running full project reset..."
	@echo ""
	@$(MAKE) clean
	@$(MAKE) clean-cache
	@$(MAKE) clean-venv
	@$(MAKE) clean-dist
	@echo ""
	@echo "$(SUCCESS) Project reset completed."

# ATENÇÃO: remove TODOS os recursos Docker não utilizados no sistema,
# incluindo imagens de outros projetos. Use com cuidado.
docker-prune:
	@echo "$(WARNING) This will remove ALL unused Docker resources on this machine."
	@echo "$(WARNING) This includes images, containers and volumes from other projects."
	@echo ""
	@printf "$(RED)Proceed? [y/N] $(NC)" && read ans && [ "$$ans" = "y" ] || (echo "Aborted." && exit 1)
	@docker system prune -af
	@echo ""
	@echo "$(SUCCESS) Unused Docker resources removed."

# =========================================================
# SHORTCUTS
# =========================================================

dtest:   docker-test
dlint:   docker-lint
dformat: docker-format