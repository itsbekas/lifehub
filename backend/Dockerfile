# ---- Build Stage ----
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

# Environment optimizations
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libmariadb3 libmariadb-dev && \
    rm -rf /var/lib/apt/lists/*

# Cache Python dependencies
COPY uv.lock pyproject.toml /app/
RUN --mount=type=cache,target=~/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Copy source code
COPY . /app

# Install project dependencies without dev dependencies
RUN --mount=type=cache,target=~/.cache/uv \
    uv sync --frozen --no-dev

# ---- Runtime Stage ----
FROM python:3.13-slim-bookworm AS runner

WORKDIR /app

# Install necessary runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmariadb3 && \
    rm -rf /var/lib/apt/lists/*

# Copy necessary files from the builder stage
COPY --from=builder /app /app

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"

# Set non-root user for security (optional, if application supports it)
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Entrypoint
CMD ["lifehub-api"]
