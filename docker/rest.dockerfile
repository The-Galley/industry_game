FROM python:3.12-slim

RUN pip install -U pip poetry \
    && poetry config virtualenvs.create false

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock /app/
RUN poetry install --no-interaction --no-ansi --without dev

COPY ./industry_game /app/industry_game

ENV PYTHONPATH=/app

EXPOSE 8000

ENTRYPOINT [ "python", "-m", "industry_game.db", "upgrade", "head" ]