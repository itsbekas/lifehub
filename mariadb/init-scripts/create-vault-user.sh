#!/bin/bash

set -u

db_name="${MYSQL_DATABASE}"
# Default variables for Vault user and password
vault_user="${VAULT_DB_USER}"
vault_password="${VAULT_DB_PASSWORD}"

# Execute the SQL commands using MariaDB's CLI tool
mariadb -u root -p"${MYSQL_ROOT_PASSWORD}" <<EOF
CREATE USER IF NOT EXISTS '${vault_user}'@'%' IDENTIFIED BY '${vault_password}';
GRANT CREATE USER, DROP, SELECT, INSERT, UPDATE, DELETE, ALTER, EXECUTE ON *.* TO '${vault_user}'@'%';
GRANT ALL PRIVILEGES ON mysql.* TO '${vault_user}'@'%';
GRANT ALL PRIVILEGES ON ${db_name}.* TO '${vault_user}'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
EOF
