#!/bin/bash

VAULT_APPROLE_ROLE_ID=$(vault read -field=role_id auth/approle/role/lifehub-app/role-id)
VAULT_APPROLE_SECRET_ID=$(vault write -f -field=secret_id auth/approle/role/lifehub-app/secret-id)
SESSION_SECRET=$(vault kv get -field=session_secret kv/lifehub-secrets/frontend)

rm -f backend/config.json

docker compose down
docker compose up --build --watch
