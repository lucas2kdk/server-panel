# Kubernetes Game Server Panel

A Kubernetes-native game server management panel inspired by Pterodactyl, designed to provide a web-based dashboard for creating, managing, and controlling game servers (initially Minecraft) within a Kubernetes cluster.

## Features

- **Kubernetes-Native**: Fully integrated with Kubernetes, leveraging StatefulSets, PersistentVolumeClaims, and native K8s APIs
- **User-Friendly**: Web-based dashboard with live console, file management, and intuitive controls
- **Live Console**: Web-based terminal with real-time log streaming and command execution
- **File Manager**: Browse and edit server files directly in the browser
- **Resource Management**: Predefined resource plans (Small, Medium, Large) with quota enforcement
- **Fine-Grained Permissions**: Role-based access control with server-level and action-level permissions
- **Multi-User Support**: Sub-user system for collaborative server management
- **Server Templates**: Pre-configured server templates (eggs) for quick deployment

## Supported Game Servers

### Minecraft
- Vanilla
- Paper/Spigot/Bukkit
- Forge
- Fabric

## Technology Stack

### Backend
- **Python 3.11+**
- **Flask 3.0+** - Web framework
- **PostgreSQL 15+** - Database
- **SQLAlchemy 2.0+** - ORM
- **Flask-Login** - Authentication
- **Flask-SocketIO** - WebSocket for console
- **Kubernetes Python Client** - K8s integration

### Frontend
- **Jinja2** - Server-side templates
- **Alpine.js** - JavaScript interactivity
- **HTMX** - AJAX interactions
- **Tailwind CSS** - Styling

### Infrastructure
- **Kubernetes 1.28+**
- **Helm 3.0+**
- **Docker**
- **GitHub Actions** - CI/CD
- **ArgoCD** - GitOps deployment
- **Prometheus + Grafana** - Monitoring

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Kubernetes cluster (local or remote)
- kubectl configured
- Helm 3.0+

### Development Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd server-panel
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt -r requirements-dev.txt
```

4. Set up environment variables:
```bash
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/serverpanel"
export SECRET_KEY="your-secret-key"
export K8S_NAMESPACE="game-servers"
```

5. Run the application:
```bash
python run.py
```

6. Access the panel at `http://localhost:5000`

### Docker Deployment

1. Build the Docker image:
```bash
docker build -t server-panel:latest .
```

2. Run with Docker Compose:
```bash
docker-compose up -d
```

### Kubernetes Deployment

1. Install the Helm chart:
```bash
helm install server-panel ./helm/server-panel -f ./helm/server-panel/values-prod.yaml
```

2. Verify deployment:
```bash
kubectl get pods -n panel
kubectl get pods -n game-servers
```

## Project Structure

```
server-panel/
├── app/                          # Flask application
│   ├── auth/                     # Authentication blueprint
│   ├── servers/                  # Server management blueprint
│   ├── console/                  # Console blueprint
│   ├── files/                    # File manager blueprint
│   ├── api/                      # REST API blueprint
│   ├── templates/                # Jinja2 templates
│   ├── static/                   # CSS, JS, images
│   └── utils/                    # Utility functions
├── helm/                         # Helm chart
├── tests/                        # Test suite
├── docs/                         # Documentation
├── ai_docs/                      # AI implementation guides
├── .github/workflows/            # GitHub Actions
└── requirements.txt              # Python dependencies
```

## Documentation

- [Project Overview](docs/PROJECT_OVERVIEW.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Requirements](docs/REQUIREMENTS.md)
- [Glossary](docs/GLOSSARY.md)
- [Deployment Guide](docs/DEPLOYMENT.md) *(coming soon)*
- [User Guide](docs/USER_GUIDE.md) *(coming soon)*
- [API Documentation](docs/API.md) *(coming soon)*

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run unit tests only
pytest tests/unit/

# Run integration tests
pytest tests/integration/
```

### Linting and Formatting

```bash
# Format code
black app/

# Lint code
flake8 app/

# Type checking
mypy app/
```

### Database Migrations

```bash
# Create a new migration
flask db migrate -m "description"

# Apply migrations
flask db upgrade

# Rollback migration
flask db downgrade
```

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Inspiration

This project is inspired by [Pterodactyl Panel](https://pterodactyl.io/), adopting features like:
- Live web console
- File manager
- Fine-grained permissions
- Server templates (eggs)
- Sub-user support

But built Kubernetes-native from the ground up.

## Roadmap

### Phase 1 - MVP (In Progress)
- [x] Project structure
- [ ] User authentication
- [ ] Server CRUD operations
- [ ] Web console
- [ ] Basic Kubernetes integration
- [ ] Helm chart
- [ ] CI/CD pipeline

### Phase 2 - Enhanced Features
- [ ] File manager
- [ ] Sub-user permissions
- [ ] Resource quotas
- [ ] Server templates

### Phase 3 - Advanced Features
- [ ] Scheduled tasks
- [ ] Backups
- [ ] Additional game types
- [ ] OAuth2 authentication

## Support

For questions, issues, or feature requests, please open an issue on GitHub.
