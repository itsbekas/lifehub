# Setting up Vault

This project requires a running instance of HashiCorp Vault. The following steps will guide you through setting up a local instance of Vault.

## Running Vault for Development

```bash
docker run --cap-add=IPC_LOCK -d --name=vault hashicorp/vault
```

## Running Vault for Production

Make sure Vault is installed and running

```bash
sudo pacman -S vault
sudo systemctl start vault
```

And set the config at `/etc/vault.hcl` to use the docker network

```hcl
listener "tcp" {
  address = "172.17.0.1:8200"
  tls_disable = 1
}
```

Then restart the vault service

```bash
sudo systemctl restart vault
```
