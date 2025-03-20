#!/bin/bash

set -e

export VAULT_ADDR=http://localhost:8200
export VAULT_APPROLE_ROLE_ID=$(vault read -field=role_id auth/approle/role/lifehub-app/role-id)
export VAULT_APPROLE_SECRET_ID=$(vault write -f -field=secret_id auth/approle/role/lifehub-app/secret-id)
export SESSION_SECRET=$(vault kv get -field=session_secret kv/lifehub-secrets/frontend)

# Setup Redis Password
export REDIS_PASSWORD=$(openssl rand -base64 32)
vault kv patch kv/lifehub/metadata redis_password=$REDIS_PASSWORD &> /dev/null

# This is the production version of the script
docker compose down
docker compose -f docker-compose.yml up --build
