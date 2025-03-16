# Setting up Infrastructure

This project requires a running instance of HashiCorp Vault. The following steps will guide you through setting up a **local Vault instance** that can be accessed by Docker containers.

---

## Running Vault for Production

### **1. Create the Vault Network**
Vault needs to be available to Docker containers but **should not be exposed to the public internet**. We create a dedicated Docker network for it:

```bash
docker network create --subnet=192.168.100.0/24 vault-net
```

### **2. Install and Start Vault**
Ensure Vault is installed and running:

```bash
sudo pacman -S vault
sudo systemctl enable --now vault
```

### **3. Configure Vault to Use the Docker Network**
Edit the Vault config file at `/etc/vault.hcl`:

```hcl
listener "tcp" {
  address = "192.168.100.1:8200"  # Private IP for Docker communication
  tls_disable = 1  # Disable TLS (use a reverse proxy or firewall to secure)
}
```

Then restart Vault to apply changes:

```bash
sudo systemctl restart vault
```

Check Vault’s status to ensure it’s running:

```bash
vault status
```

### **4. Start the Application with Docker Compose**
Run the following command to start the backend and frontend services:

```bash
docker-compose up -d
```

This will ensure the backend is connected to the Vault network (`vault-net`).

### **5. Test Vault Connectivity from Backend**
Run this command inside the backend container to verify Vault is reachable:

```bash
docker run --rm --network=vault-net curlimages/curl:latest -L -v http://192.168.100.1:8200/v1/sys/health
```

A successful response means Vault is **properly set up** and accessible.
