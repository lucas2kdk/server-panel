# Contributing to Server Panel

Thank you for your interest in contributing! This guide will help you get started.

## Development Setup

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Docker and Docker Compose (optional)
- kubectl and access to a Kubernetes cluster (optional, for testing K8s integration)

### Local Development

1. **Clone the repository**:
```bash
git clone https://github.com/lucas2kdk/server-panel.git
cd server-panel
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt -r requirements-dev.txt
```

4. **Set up environment variables**:
```bash
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/serverpanel"
export SECRET_KEY="dev-secret-key"
export K8S_NAMESPACE="game-servers"
export K8S_IN_CLUSTER="false"
```

5. **Start PostgreSQL** (using Docker):
```bash
docker run --name server-panel-db \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=serverpanel \
  -p 5432:5432 \
  -d postgres:15-alpine
```

Or use docker-compose:
```bash
docker-compose up -d postgres
```

6. **Run the application**:
```bash
python run.py
```

7. **Access the application**:
   - Open http://localhost:5000
   - Register a new account
   - Create your first server!

## Code Quality

### Before Committing

**Always run these commands before committing**:

```bash
# Format code with Black
black app/

# Check linting
flake8 app/

# Run type checking
mypy app/ --ignore-missing-imports

# Run tests
pytest
```

### Code Style

- **Formatting**: We use [Black](https://black.readthedocs.io/) with 100 character line length
- **Linting**: We use [Flake8](https://flake8.pycqa.org/)
- **Type Hints**: We use [mypy](https://mypy.readthedocs.io/) for static type checking
- **Docstrings**: Use Google-style docstrings

### Example

```python
def create_server(name: str, server_type: str, resources: dict) -> Server:
    """Create a new Minecraft server.

    Args:
        name: Human-readable server name
        server_type: Type of server (vanilla, paper, etc.)
        resources: Dict with cpu_cores, ram_mb, disk_gb

    Returns:
        Created Server instance

    Raises:
        QuotaExceededError: If user has insufficient quota
        KubernetesError: If server creation fails
    """
    # Implementation here
    pass
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/test_models.py -v

# Run tests with specific marker
pytest -m unit
```

### Writing Tests

- Place unit tests in `tests/unit/`
- Place integration tests in `tests/integration/`
- Use fixtures from `tests/conftest.py`
- Aim for >80% code coverage

Example test:
```python
def test_server_creation(test_user, init_database):
    """Test that servers can be created successfully."""
    server = Server(
        name="Test Server",
        owner_id=test_user.id,
        server_type="paper",
        server_version="1.20.1",
        cpu_cores=2,
        ram_mb=4096,
        disk_gb=20
    )
    init_database.session.add(server)
    init_database.session.commit()

    assert server.id is not None
    assert server.name == "Test Server"
```

## Git Workflow

### Branches

- `main` - Production-ready code
- `develop` - Development branch
- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `hotfix/*` - Urgent production fixes

### Commit Messages

Follow conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Formatting, missing semicolons, etc.
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance tasks

Examples:
```bash
git commit -m "feat(servers): Add support for Forge mod loader"
git commit -m "fix(auth): Resolve password reset email bug"
git commit -m "docs(api): Update API endpoint documentation"
```

### Pull Request Process

1. **Create a feature branch**:
```bash
git checkout -b feature/add-forge-support
```

2. **Make your changes**:
   - Write code
   - Add tests
   - Update documentation

3. **Ensure code quality**:
```bash
black app/
flake8 app/
pytest
```

4. **Commit your changes**:
```bash
git add .
git commit -m "feat(servers): Add Forge mod loader support"
```

5. **Push to GitHub**:
```bash
git push origin feature/add-forge-support
```

6. **Create Pull Request**:
   - Go to GitHub repository
   - Click "New Pull Request"
   - Select your branch
   - Fill in PR template
   - Request review

7. **Address review feedback**:
   - Make requested changes
   - Push additional commits
   - Re-request review

8. **Merge**:
   - Squash and merge when approved
   - Delete feature branch

## Project Structure

```
server-panel/
├── app/                  # Main application code
│   ├── auth/            # Authentication
│   ├── servers/         # Server management
│   ├── console/         # Console access
│   ├── files/           # File manager
│   ├── api/             # REST API
│   ├── models.py        # Database models
│   └── config.py        # Configuration
├── tests/               # Test suite
│   ├── unit/           # Unit tests
│   └── integration/    # Integration tests
├── helm/               # Kubernetes deployment
└── docs/               # Documentation
```

## Debugging

### Enable Debug Mode

```bash
export FLASK_ENV=development
python run.py
```

### Database Debugging

```python
# Enable SQL query logging
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
```

### Kubernetes Debugging

```bash
# Check pods
kubectl get pods -n game-servers

# View logs
kubectl logs <pod-name> -n game-servers

# Describe pod
kubectl describe pod <pod-name> -n game-servers

# Exec into pod
kubectl exec -it <pod-name> -n game-servers -- /bin/sh
```

## Common Issues

### Import Errors
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Database Connection Errors
- Check PostgreSQL is running: `docker ps`
- Verify DATABASE_URL is correct
- Check database exists: `psql -U postgres -l`

### Kubernetes API Errors
- Verify kubeconfig: `kubectl config view`
- Check namespace exists: `kubectl get namespace game-servers`
- Verify RBAC permissions

### Test Failures
- Check database is running
- Ensure test database is clean
- Verify environment variables are set

## Documentation

### Updating Documentation

- Code comments for complex logic
- Docstrings for all functions and classes
- Update README.md for user-facing changes
- Update API.md for API changes
- Add examples for new features

### Building Documentation

```bash
# Generate API docs (if using Sphinx)
cd docs
make html
```

## Release Process

1. **Update version** in `helm/server-panel/Chart.yaml`
2. **Update CHANGELOG.md**
3. **Create release tag**:
```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```
4. **GitHub Actions** will automatically:
   - Build Docker image
   - Package Helm chart
   - Create GitHub release

## Getting Help

- **Issues**: https://github.com/lucas2kdk/server-panel/issues
- **Discussions**: https://github.com/lucas2kdk/server-panel/discussions
- **Email**: lucas@rosenvold.tech

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the project
- Show empathy towards other contributors

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
