FROM astral/uv:python3.10-bookworm AS base

WORKDIR /app
COPY ../uv.lock ../pyproject.toml ../README.md /app/

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_TOOL_BIN_DIR=/usr/local/bin
ENV UV_PYTHON_DOWNLOADS=0

RUN apt-get update \
    && apt-get upgrade --no-install-recommends -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

FROM base AS dev
COPY --from=base --chown=app:app /app /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project
COPY ./disco_bot ./disco_bot/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

FROM base AS prod
COPY --from=dev --chown=app:app /app /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=../uv.lock,target=uv.lock \
    --mount=type=bind,source=../pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev
COPY ./disco_bot/ ./disco_bot/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT []

CMD ["python", "-m", "disco_bot.main"]
