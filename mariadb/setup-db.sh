#!/bin/bash

db_name=lifehub

db_user=lifehub
db_password=testing

vault_user=vault
vault_password=vault-testing

# Must be root to run this script
if [ "$(id -u)" -ne 0 ]; then
  echo "Error: This script must be run as root"
  exit 1
fi

# Check if mariadb is running
if ! mariadb-admin ping -h localhost --silent; then
  echo "Error: MariaDB is not running"
  exit 1
fi

# Setup the database and user for the application
mariadb -u root <<EOF
CREATE DATABASE IF NOT EXISTS ${db_name};
CREATE USER IF NOT EXISTS '${db_user}'@'%' IDENTIFIED BY '${db_password}';
GRANT ALL PRIVILEGES ON ${db_name}.* TO '${db_user}'@'%';
FLUSH PRIVILEGES;
EOF

# Setup Vault user and grant privileges
# This user is used by the Vault server to create ephemeral users for applications
mariadb -u root <<EOF
CREATE USER IF NOT EXISTS '${vault_user}'@'%' IDENTIFIED BY '${vault_password}';
GRANT CREATE USER, DROP, SELECT, INSERT, UPDATE, DELETE, ALTER, EXECUTE ON *.* TO '${vault_user}'@'%';
GRANT ALL PRIVILEGES ON mysql.* TO '${vault_user}'@'%';
GRANT ALL PRIVILEGES ON ${db_name}.* TO '${vault_user}'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
EOF
