bootstrap:
	docker compose build

up:
	docker compose up --build -d

demo:
	docker compose run --rm app python src/pipeline.py

test:
	docker compose run --rm -e PYTHONPATH=/app app python -m pytest tests --cov=src --cov-report=term-missing

down:
	docker compose down