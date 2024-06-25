FROM python:3.10.13-slim-bookworm AS base

ENV PYTHONBUFFERED=1
ENV POETRY_VERSION=1.8.3
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

RUN apt-get update \
    && apt-get upgrade -y
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
		&& $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /app

COPY ../poetry.lock ../pyproject.toml .

FROM base AS dev
COPY --from=base /app /app
RUN poetry install --no-interaction --no-cache
COPY ./src ./src/

FROM base AS prod
COPY --from=base /app /app
RUN poetry install --no-interaction --no-cache --without dev
COPY ./src/ ./src/

CMD ["poetry", "run", "python", "src/main.py"]
