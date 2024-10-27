#!/bin/bash

export UV_PROJECT_ENVIRONMENT=.venv-dev

uv venv
VIRTUAL_ENV="${UV_PROJECT_ENVIRONMENT}" uv pip install -e .

exec uv run lifehub-api