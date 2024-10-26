FROM ghcr.io/astral-sh/uv:python3.13-bookworm
WORKDIR /app
COPY . .
RUN uv venv
RUN uv pip install .
CMD ["uv", "run", "lifehub-api"]
EXPOSE 8000
