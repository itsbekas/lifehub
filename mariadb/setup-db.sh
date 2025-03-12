#!/bin/bash

db_name=lifehub

db_user=lifehub
db_password=testing

vault_user="vault"
vault_password="vault-testing"

# Must be root to run this script
if [ "$(id -u)" -ne 0 ]; then
  echo "Error: This script must be run as root"
  exit 1
fi

# Check if mariadb is running
echo "Checking if MariaDB is running..."
if ! mariadb-admin ping -h localhost --silent; then
  echo "Error: MariaDB is not running"
  exit 1
fi

# Setup the database and user for the application
echo "Setting up database and user..."
mariadb -u root <<EOF
CREATE DATABASE IF NOT EXISTS ${db_name};
CREATE USER IF NOT EXISTS '${db_user}'@'%' IDENTIFIED BY '${db_password}';
GRANT ALL PRIVILEGES ON ${db_name}.* TO '${db_user}'@'%';
FLUSH PRIVILEGES;
EOF

# Check if the database was created
if ! mariadb -u root -e "USE ${db_name}"; then
  echo "Error: Failed to create database"
  exit 1
fi

# Check if the user was created
if ! mariadb -u root -e "SELECT User FROM mysql.user WHERE User='${db_user}'"; then
  echo "Error: Failed to create user"
  exit 1
fi

# Setup Vault user and grant privileges
# This user is used by the Vault server to create ephemeral users for applications
echo "Setting up Vault user and granting privileges..."
mariadb -u root <<EOF
CREATE USER IF NOT EXISTS '${vault_user}'@'%' IDENTIFIED BY '${vault_password}';
GRANT CREATE USER, DROP, SELECT, INSERT, UPDATE, DELETE, ALTER, EXECUTE ON *.* TO '${vault_user}'@'%';
GRANT ALL PRIVILEGES ON mysql.* TO '${vault_user}'@'%';
GRANT ALL PRIVILEGES ON ${db_name}.* TO '${vault_user}'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
EOF

# Check if the Vault user was created
if ! mariadb -u root -e "SELECT User FROM mysql.user WHERE User='${vault_user}'"; then
  echo "Error: Failed to create Vault user"
  exit 1
fi

# Check if the Vault user has the correct privileges
if ! mariadb -u root -e "SHOW GRANTS FOR '${vault_user}'@'%'"; then
  echo "Error: Failed to grant privileges to Vault user"
  exit 1
fi

echo "Database setup complete"
