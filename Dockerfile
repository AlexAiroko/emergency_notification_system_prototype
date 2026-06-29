FROM python:3.12-slim

# system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# poetry installation
RUN pip install poetry==2.3.4

# disabling the virtual environment (IMPORTANT for docker)
ENV POETRY_VENV_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1

WORKDIR /app

# project dependencies
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false

RUN poetry install --only main --no-root

# copying the code
COPY . .

# launching via uvicorn
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
