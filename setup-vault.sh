#!/bin/bash

# set -e  # Exit on error
set -u  # Treat unset variables as errors
set -o pipefail  # Catch pipeline errors

# Vault address and login
VAULT_ADDR="http://localhost:8200"
export VAULT_ADDR

# Always make sure these are synced with the backend config
DB_NAME="lifehub"
DB_HOST="localhost"
VAULT_DB_USER="vault"
VAULT_DB_ROLE="lifehub-app"
VAULT_DB_ADMIN_ROLE="lifehub-admin"
VAULT_DB_ADMIN_READONLY_ROLE="lifehub-admin-readonly"
VAULT_DB_MOUNT_POINT="database/lifehub"

# --- Enable Secrets Engines ---
echo "Enabling Transit Engine..."
vault secrets enable -path=transit/lifehub transit &> /dev/null || echo "Transit engine already enabled."

echo "Enabling KV v2 Engine..."
vault secrets enable -path=kv/lifehub kv-v2 &> /dev/null || echo "KV v2 engine already enabled."

echo "Enabling Database Engine..."
vault secrets enable -path="$VAULT_DB_MOUNT_POINT" database &> /dev/null || echo "Database engine already enabled."

# --- Configure Database Secret Engine ---
echo "Retrieving vault db secrets..."
VAULT_DB_PASSWORD="$(vault kv get -field=password kv/vault-metadata/mariadb)"

echo "Checking if database connection is already configured..."
if ! vault read "$VAULT_DB_MOUNT_POINT/config/$DB_NAME" &>/dev/null; then
    echo "Configuring database connection..."
    vault write "$VAULT_DB_MOUNT_POINT/config/$DB_NAME" \
        plugin_name="mysql-database-plugin" \
        connection_url="{{username}}:{{password}}@tcp($DB_HOST:3306)/" \
        allowed_roles="$VAULT_DB_ROLE","$VAULT_DB_ADMIN_ROLE","$VAULT_DB_ADMIN_READONLY_ROLE" \
        username="$VAULT_DB_USER" \
        password="$VAULT_DB_PASSWORD"
else
    echo "Database connection already configured."
fi

# --- Create Database Roles ---
echo "Checking existing database roles..."
EXISTING_ROLES=$(vault list "$VAULT_DB_MOUNT_POINT/roles" | tail -n +3)

# With the exception of the admin read-only role, which runs on localhost,
# these roles are meant for the docker network, so we use a limited host wildcard: 172.%.
if [[ ! "$EXISTING_ROLES" =~ "$VAULT_DB_ROLE" ]]; then
    echo "Creating database role: $VAULT_DB_ROLE"
    vault write "$VAULT_DB_MOUNT_POINT/roles/$VAULT_DB_ROLE" \
        db_name="$DB_NAME" \
        creation_statements="CREATE USER '{{name}}'@'172.%' IDENTIFIED BY '{{password}}'; GRANT SELECT, INSERT, UPDATE, DELETE ON $DB_NAME.* TO '{{name}}'@'172.%';" \
        default_ttl="5m" \
        max_ttl="10m"
else
    echo "Database role '$VAULT_DB_ROLE' already exists."
fi

if [[ ! "$EXISTING_ROLES" =~ "$VAULT_DB_ADMIN_ROLE" ]]; then
    echo "Creating database admin role: $VAULT_DB_ADMIN_ROLE"
    vault write "$VAULT_DB_MOUNT_POINT/roles/$VAULT_DB_ADMIN_ROLE" \
        db_name="$DB_NAME" \
        creation_statements="CREATE USER '{{name}}'@'172.%' IDENTIFIED BY '{{password}}'; GRANT ALL PRIVILEGES ON $DB_NAME.* TO '{{name}}'@'172.%'; GRANT GRANT OPTION ON $DB_NAME.* TO '{{name}}'@'172.%';" \
        default_ttl="5m" \
        max_ttl="10m"
else
    echo "Database admin role '$VAULT_DB_ADMIN_ROLE' already exists."
fi

if [[ ! "$EXISTING_ROLES" =~ "$VAULT_DB_ADMIN_READONLY_ROLE" ]]; then
    echo "Creating database admin readonly role: $VAULT_DB_ADMIN_READONLY_ROLE"
    vault write "$VAULT_DB_MOUNT_POINT/roles/$VAULT_DB_ADMIN_READONLY_ROLE" \
        db_name="$DB_NAME" \
        creation_statements="CREATE USER '{{name}}'@'localhost' IDENTIFIED BY '{{password}}'; GRANT SELECT ON $DB_NAME.* TO '{{name}}'@'localhost';" \
        default_ttl="1h" \
        max_ttl="2h"
else
    echo "Database admin readonly role '$VAULT_DB_ADMIN_READONLY_ROLE' already exists."
fi

# --- Setup Vault Policies ---
echo "Applying lifehub-user policy..."
vault policy write lifehub-user - <<EOF
# Allow users to encrypt data using only their own KEK
path "transit/lifehub/encrypt/user-{{identity.entity.id}}" {
    capabilities = ["update"]
}

# Allow users to decrypt data using only their own KEK
path "transit/lifehub/decrypt/user-{{identity.entity.id}}" {
    capabilities = ["update"]
}

# Allow users to read metadata about their own KEK from Vault KV
path "kv/lifehub/user-keys/{{identity.entity.id}}" {
    capabilities = ["read"]
}
EOF

echo "Applying lifehub-app policy..."
vault policy write lifehub-app - <<EOF
# Backend can encrypt data using any user's KEK
path "transit/lifehub/encrypt/user-*" {
    capabilities = ["update"]
}

# Backend can decrypt data using any user's KEK
path "transit/lifehub/decrypt/user-*" {
    capabilities = ["update"]
}

# Backend can create, update, read, and delete user KEKs
path "transit/lifehub/keys/user-*" {
    capabilities = ["create", "update", "read", "delete"]
}

# Backend has full access to all data in the lifehub KV store
path "kv/lifehub/*" {
    capabilities = ["create", "update", "read", "delete"]
}

# Backend can read and write to the lifehub database
path "database/lifehub/*" {
    capabilities = ["create", "read", "update", "delete"]
}
EOF

# --- Setup Vault Auth Methods ---
echo "Enabling AppRole authentication..."
vault auth enable approle &> /dev/null || echo "AppRole authentication already enabled."

echo "Creating AppRole for lifehub-app..."
vault write auth/approle/role/lifehub-app \
    token_policies="lifehub-app" \
    token_ttl="11m" \
    token_max_ttl="31d" \
    secret_id_num_uses="0" &> /dev/null

echo "Vault setup completed successfully!"
