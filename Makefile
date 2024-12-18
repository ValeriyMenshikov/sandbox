.DEFAULT_GOAL := help

run:
	@echo "run server"
	uvicorn application.main:main_app --host 0.0.0.0 --port 85 --reload

format:
	@echo "format"
	poetry run ruff format
	poetry run ruff check --fix .

lint:
	@echo "lint"
	poetry run mypy .

help:
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}'; {printf "  %-20s %s\n", $$1, $$2}'