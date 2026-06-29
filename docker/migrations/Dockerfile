FROM python:3.12-slim

WORKDIR /app

# poetry installation
RUN pip install poetry==2.3.4

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

# copy only the dependencies first (for the cache)
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false

RUN poetry install --only main --no-root

# copying the code (including alembic)
COPY . .

# launching migrations
CMD ["poetry", "run", "alembic", "upgrade", "head"]
