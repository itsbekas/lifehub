#!/bin/bash

set -e  # Exit on error
set -u  # Treat unset variables as errors
set -o pipefail  # Catch pipeline errors

# Vault address and login
VAULT_ADDR="http://192.168.100.1:8200"
export VAULT_ADDR

# Always make sure these are synced with the backend config
DB_NAME="lifehub"
DB_HOST="192.168.100.1"
VAULT_DB_USER="vault"
VAULT_DB_PASSWORD="vault-testing"
VAULT_DB_ROLE="lifehub-app"
VAULT_DB_ADMIN_ROLE="lifehub-admin"
VAULT_DB_MOUNT_POINT="database/lifehub"

# --- Enable Secrets Engines ---
echo "Enabling Transit Engine..."
vault secrets enable -path=transit/lifehub transit &> /dev/null || echo "Transit engine already enabled."

echo "Enabling KV v2 Engine..."
vault secrets enable -path=kv/lifehub kv-v2 &> /dev/null || echo "KV v2 engine already enabled."

echo "Enabling Database Engine..."
vault secrets enable -path="$VAULT_DB_MOUNT_POINT" database &> /dev/null || echo "Database engine already enabled."

# --- Configure Database Secret Engine ---
echo "Checking if database connection is already configured..."
if ! vault read "$VAULT_DB_MOUNT_POINT/config/$DB_NAME" &>/dev/null; then
    echo "Configuring database connection..."
    vault write "$VAULT_DB_MOUNT_POINT/config/$DB_NAME" \
        plugin_name="mysql-database-plugin" \
        connection_url="{{username}}:{{password}}@tcp($DB_HOST:3306)/" \
        allowed_roles="$VAULT_DB_ROLE","$VAULT_DB_ADMIN_ROLE" \
        username="$VAULT_DB_USER" \
        password="$VAULT_DB_PASSWORD"
else
    echo "Database connection already configured."
fi

# --- Create Database Roles ---
echo "Checking existing database roles..."
EXISTING_ROLES=$(vault list "$VAULT_DB_MOUNT_POINT/roles" | tail -n +3)

if [[ ! "$EXISTING_ROLES" =~ "$VAULT_DB_ROLE" ]]; then
    echo "Creating database role: $VAULT_DB_ROLE"
    vault write "$VAULT_DB_MOUNT_POINT/roles/$VAULT_DB_ROLE" \
        db_name="$DB_NAME" \
        creation_statements="CREATE USER '{{name}}'@'%' IDENTIFIED BY '{{password}}'; GRANT SELECT, INSERT, UPDATE, DELETE ON $DB_NAME.* TO '{{name}}'@'%';" \
        default_ttl="1h" \
        max_ttl="24h"
else
    echo "Database role '$VAULT_DB_ROLE' already exists."
fi

if [[ ! "$EXISTING_ROLES" =~ "$VAULT_DB_ADMIN_ROLE" ]]; then
    echo "Creating database admin role: $VAULT_DB_ADMIN_ROLE"
    vault write "$VAULT_DB_MOUNT_POINT/roles/$VAULT_DB_ADMIN_ROLE" \
        db_name="$DB_NAME" \
        creation_statements="CREATE USER '{{name}}'@'%' IDENTIFIED BY '{{password}}'; GRANT ALL PRIVILEGES ON $DB_NAME.* TO '{{name}}'@'%'; GRANT GRANT OPTION ON $DB_NAME.* TO '{{name}}'@'%';" \
        default_ttl="1h" \
        max_ttl="2h"
else
    echo "Database admin role '$VAULT_DB_ADMIN_ROLE' already exists."
fi

# --- Setup Vault Policies ---
echo "Applying user-keystore policy..."
vault policy write user-keystore - <<EOF
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

echo "Applying backend-keystore policy..."
vault policy write backend-keystore - <<EOF
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

# Backend has full access to all user KEK metadata in Vault KV
path "kv/lifehub/user-keys/*" {
    capabilities = ["create", "update", "read", "delete"]
}
EOF

echo "Vault setup completed successfully!"
