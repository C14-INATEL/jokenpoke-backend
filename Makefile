run:
	uvicorn app.main:app --reload

test:
	pytest -v

test-coverage:
	pytest --cov=app

build:
	docker compose build

up:
	docker compose up

down:
	docker compose down

format:
	black .

lint:
	ruff check .

check:
	ruff check . && pytest