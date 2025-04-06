# LifeHub

LifeHub is a comprehensive personal finance and life management platform that helps you track your finances, manage budgets, and connect to your bank accounts securely.

![LifeHub Dashboard](https://placeholder-for-dashboard-screenshot.com)

## Project Overview

LifeHub is designed to be your central hub for personal finance management. It provides a unified interface to:

- Connect to your bank accounts securely using open banking APIs
- Track transactions and categorize spending
- Create and manage budgets
- Visualize your financial data with intuitive charts and reports
- Plan and track financial goals

The application is built with a focus on security, user experience, and extensibility.

## Tech Stack

### Backend

- **Python 3.10+**: Core programming language
- **FastAPI**: High-performance web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM for database interactions
- **Pydantic**: Data validation and settings management
- **Alembic**: Database migration tool
- **PostgreSQL**: Primary database for persistent storage
- **HashiCorp Vault**: Secure storage for sensitive information and encryption keys
- **Redis**: In-memory data store for caching and session management

### Frontend

- **TypeScript**: Type-safe JavaScript for frontend development
- **React**: UI library for building component-based interfaces
- **TanStack Router**: Type-safe routing for React applications
- **TanStack Query**: Data fetching and state management
- **Mantine UI**: Component library for building modern interfaces
- **Vite**: Next-generation frontend tooling for fast development

### Infrastructure

- **Docker**: Containerization for consistent development and deployment
- **Docker Compose**: Multi-container application orchestration

## Key Features

### Secure Bank Integration

LifeHub uses open banking APIs to securely connect to your bank accounts. The platform never stores your banking credentials - instead, it uses OAuth-based authentication flows to securely access your financial data.

### Transaction Management

- Automatic categorization of transactions (Planned)
- Manual recategorization with persistent rules
- Search and filter transactions by date, amount, category, and more

### Budget Management

- Create categories and subcategories for budgeting
- Set monthly budget limits for each category
- Track spending against budgets
- Visual indicators for budget status

### Data Security

- End-to-end encryption for sensitive financial data
- Secure key management with HashiCorp Vault
- No storage of banking credentials
- HTTPS for all communications

## Architecture

LifeHub follows a modern client-server architecture:

1. **Backend API**: A RESTful API built with FastAPI that handles data processing, storage, and integration with banking APIs
2. **Frontend SPA**: A single-page application built with React that provides the user interface
3. **Database**: PostgreSQL for persistent storage of user data and transaction information
4. **Vault**: HashiCorp Vault for secure storage of encryption keys and sensitive configuration

## Getting Started

### Prerequisites

- Docker and Docker Compose
- HashiCorp Vault (for development, can be run in Docker)

### Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/itsbekas/lifehub.git
   cd lifehub
   ```

2. Set up Vault (see Infrastructure section below)

3. Start the development environment:
   ```bash
   ./run-dev.sh
   ```

4. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Infrastructure Setup

### Setting up Vault

This project requires a running instance of HashiCorp Vault. The following steps will guide you through setting up a **local Vault instance** that can be accessed by Docker containers.

#### **1. Create the Vault Network**
Vault needs to be available to Docker containers but **should not be exposed to the public internet**. We create a dedicated Docker network for it:

```bash
docker network create --subnet=192.168.100.0/24 vault-net
```

#### **2. Install and Start Vault**
Ensure Vault is installed and running:

```bash
sudo pacman -S vault
sudo systemctl enable --now vault
```

#### **3. Configure Vault to Use the Docker Network**
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

Check Vault's status to ensure it's running:

```bash
vault status
```

#### **4. Start the Application with Docker Compose**
Run the following command to start the backend and frontend services:

```bash
docker-compose up -d
```

This will ensure the backend is connected to the Vault network (`vault-net`).

#### **5. Test Vault Connectivity from Backend**
Run this command inside the backend container to verify Vault is reachable:

```bash
docker run --rm --network=vault-net curlimages/curl:latest -L -v http://192.168.100.1:8200/v1/sys/health
```

A successful response means Vault is **properly set up** and accessible.

## Project Structure

```
lifehub/
├── backend/                # Python FastAPI backend
│   ├── lifehub/            # Main application package
│   │   ├── core/           # Core functionality and utilities
│   │   ├── modules/        # Feature modules (finance, etc.)
│   │   └── main.py         # Application entry point
│   └── Dockerfile          # Backend container definition
├── frontend/               # React TypeScript frontend
│   ├── public/             # Static assets
│   ├── src/                # Source code
│   │   ├── components/     # Reusable UI components
│   │   ├── hooks/          # Custom React hooks
│   │   ├── lib/            # Utilities and helpers
│   │   ├── routes/         # Application routes
│   │   └── styles/         # CSS and styling
│   └── Dockerfile          # Frontend container definition
└── docker-compose.yml      # Container orchestration
```

## Future Plans

- Mobile application with React Native
- Expense forecasting and financial planning tools
- Investment portfolio tracking
- Goal-based savings features
- Multi-currency support
