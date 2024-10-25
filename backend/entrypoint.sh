#!/bin/bash

uv venv .venv-dev
source .venv-dev/bin/activate
uv pip install -e .

exec uv run lifehub-api
