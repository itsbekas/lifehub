FROM mariadb:latest

# Install the HashiCorp Key Management plugin
RUN apt-get update && \
    apt-get install -y mariadb-plugin-hashicorp-key-management && \
    rm -rf /var/lib/apt/lists/*

COPY config/vault.cnf /etc/mysql/mariadb.conf.d/vault.cnf

ARG VAULT_TOKEN
ARG VAULT_URL

RUN sed -i "s|@VAULT_TOKEN@|${VAULT_TOKEN}|g" /etc/mysql/mariadb.conf.d/vault.cnf
RUN sed -i "s|@VAULT_URL@|${VAULT_URL}|g" /etc/mysql/mariadb.conf.d/vault.cnf
