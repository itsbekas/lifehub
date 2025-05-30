#!/bin/bash

set -e

source .env
vault operator unseal $VAULT_KEY
vault login $VAULT_TOKEN

export VAULT_ADDR=http://localhost:8200
export VAULT_APPROLE_ROLE_ID=$(vault read -field=role_id auth/approle/role/lifehub-app/role-id)
export VAULT_APPROLE_SECRET_ID=$(vault write -f -field=secret_id auth/approle/role/lifehub-app/secret-id)
export SESSION_SECRET=$(vault kv get -field=session_secret kv/lifehub-secrets/frontend)

# Setup Redis Password
export REDIS_PASSWORD=$(openssl rand -base64 32)
vault kv patch kv/lifehub/metadata redis_password=$REDIS_PASSWORD &> /dev/null

rm -f backend/config.json

docker compose down
docker compose up --build --watch
