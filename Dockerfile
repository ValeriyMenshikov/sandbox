FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock /app/
COPY application /app/application

RUN pip install poetry
RUN poetry install --no-interaction --no-ansi

CMD ["poetry", "run", "uvicorn", "application.main:main_app", "--host", "0.0.0.0", "--port", "8085", "--reload"]