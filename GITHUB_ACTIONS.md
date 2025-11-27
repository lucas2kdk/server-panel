# GitHub Actions CI/CD Setup

This document describes the GitHub Actions workflows implemented for the Kubernetes Game Server Panel.

## Overview

Three automated workflows have been configured to handle continuous integration, Docker image building, and release management:

1. **CI Workflow** - Linting, testing, and security scanning
2. **Build Workflow** - Docker image creation and publishing
3. **Release Workflow** - Helm chart packaging and distribution

## Workflow Details

### 1. CI Workflow (`.github/workflows/ci.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

**Jobs:**

#### Lint Job
- **Black** - Code formatting verification
- **Flake8** - Style guide enforcement and error detection
- **mypy** - Static type checking

#### Test Job
- Runs pytest with PostgreSQL test database
- Generates code coverage reports (term, HTML, XML)
- Uploads coverage to Codecov
- Enforces minimum 50% test coverage

#### Security Job
- **Safety** - Checks dependencies for known vulnerabilities
- **Bandit** - Security linter for Python code
- Uploads security reports as artifacts

**Status Badge:**
```markdown
[![CI - Lint and Test](https://github.com/YOUR_USERNAME/server-panel/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/server-panel/actions/workflows/ci.yml)
```

### 2. Build Workflow (`.github/workflows/build.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Push to tags matching `v*.*.*`
- Pull requests to `main` branch

**Jobs:**

#### Build and Push Job
- Multi-platform builds (linux/amd64, linux/arm64)
- Pushes images to GitHub Container Registry (ghcr.io)
- Uses Docker BuildKit caching for faster builds
- Automatic tagging strategy:
  - Branch name (e.g., `main`, `develop`)
  - Semantic version tags (e.g., `v1.2.3`, `v1.2`, `v1`)
  - Git SHA with branch prefix
  - `latest` tag for default branch

#### Scan Job
- **Trivy** vulnerability scanner
- Uploads results to GitHub Security tab
- Runs only on non-PR builds

**Status Badge:**
```markdown
[![Build and Push Docker Image](https://github.com/YOUR_USERNAME/server-panel/actions/workflows/build.yml/badge.svg)](https://github.com/YOUR_USERNAME/server-panel/actions/workflows/build.yml)
```

### 3. Release Workflow (`.github/workflows/release.yml`)

**Triggers:**
- Push to tags matching `v*.*.*`
- Manual workflow dispatch with version input

**Jobs:**

#### Release Helm Chart Job
- Updates Chart.yaml with version and appVersion
- Lints Helm chart
- Packages chart as .tgz file
- Creates GitHub Release with chart artifact
- Pushes chart to GitHub Container Registry OCI repository

#### Update Deployment Docs Job
- Updates CHANGELOG.md with release information
- Commits changes back to repository

**Status Badge:**
```markdown
[![Release - Helm Chart](https://github.com/YOUR_USERNAME/server-panel/actions/workflows/release.yml/badge.svg)](https://github.com/YOUR_USERNAME/server-panel/actions/workflows/release.yml)
```

## Configuration Files

### pytest.ini
- Test discovery configuration
- Coverage settings
- Test markers (unit, integration, slow, kubernetes)
- Warning filters

### .flake8
- Max line length: 127 characters
- Complexity limit: 10
- Excluded directories and patterns
- Per-file ignore rules

### pyproject.toml
- Black configuration (100 character line length)
- mypy settings
- Coverage report configuration
- Pytest options

## Testing Infrastructure

### Test Organization
```
tests/
├── __init__.py
├── conftest.py              # Pytest fixtures
├── unit/
│   ├── __init__.py
│   ├── test_models.py       # Database model tests
│   └── test_auth.py         # Authentication tests
└── integration/
    └── __init__.py
```

### Fixtures (conftest.py)
- `app` - Flask application for testing
- `client` - Test client for HTTP requests
- `init_database` - Database setup and teardown
- `test_user` - Regular test user
- `admin_user` - Admin test user

### Unit Tests

#### test_models.py
- Password hashing verification
- Resource usage calculation
- Quota checking logic
- Kubernetes name generation
- Server serialization

#### test_auth.py
- Login page accessibility
- Registration page accessibility
- Successful registration
- Duplicate email handling
- Successful login
- Failed login scenarios

## Using the Workflows

### Running Locally

#### Run Linters
```bash
# Format code
black app/

# Check formatting
black --check app/

# Run Flake8
flake8 app/

# Run mypy
mypy app/ --ignore-missing-imports
```

#### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/test_models.py -v

# Run tests with marker
pytest -m unit
```

#### Build Docker Image
```bash
docker build -t server-panel:test .
```

### Triggering Workflows

#### CI Workflow
- Push to main/develop or create pull request
- Workflow runs automatically

#### Build Workflow
- Push to main/develop: Builds and pushes image
- Create tag `v1.0.0`: Builds release image
- Create PR: Builds but doesn't push

#### Release Workflow
```bash
# Create and push tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

Or manually:
1. Go to Actions tab in GitHub
2. Select "Release - Helm Chart" workflow
3. Click "Run workflow"
4. Enter version number

## Required GitHub Secrets

The workflows use the built-in `GITHUB_TOKEN` which is automatically provided. No additional secrets are required for basic functionality.

### Optional Secrets

For enhanced features, you can add:

- `CODECOV_TOKEN` - For private repository coverage uploads
- Custom secrets for additional integrations

## Workflow Permissions

The workflows require these permissions:

### CI Workflow
- `contents: read` - Checkout code
- `packages: read` - Pull base images (if needed)

### Build Workflow
- `contents: read` - Checkout code
- `packages: write` - Push Docker images to GHCR

### Release Workflow
- `contents: write` - Create GitHub releases
- `packages: write` - Push Helm charts to GHCR

These are configured in each workflow file and managed by GitHub.

## Monitoring Workflows

### View Workflow Runs
1. Navigate to repository on GitHub
2. Click "Actions" tab
3. Select workflow from sidebar
4. View run history and details

### Debugging Failed Workflows
1. Click on failed workflow run
2. Expand failed job
3. Review step logs
4. Check for error messages
5. Re-run failed jobs if needed

## Next Steps

### Before First Run

1. **Update README badges** - Replace `YOUR_USERNAME` with your GitHub username
2. **Push to GitHub** - Workflows will trigger on first push
3. **Review first runs** - Check that all jobs pass
4. **Configure branch protection** - Require CI to pass before merging

### Enhancements

- Add integration tests for Kubernetes operations
- Configure Codecov for coverage tracking
- Add deployment workflow for staging environment
- Implement semantic versioning automation
- Add changelog generation

## Troubleshooting

### Common Issues

**Tests failing locally but passing in CI:**
- Check Python version (should be 3.11)
- Verify database is running
- Check environment variables

**Docker build failing:**
- Verify Dockerfile syntax
- Check base image availability
- Review build logs for dependency errors

**Helm chart packaging failing:**
- Run `helm lint helm/server-panel` locally
- Check Chart.yaml syntax
- Verify all template files exist

**Coverage too low:**
- Add more unit tests
- Adjust coverage threshold in ci.yml
- Review coverage report: `coverage report -m`

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Build Push Action](https://github.com/docker/build-push-action)
- [Pytest Documentation](https://docs.pytest.org/)
- [Helm Documentation](https://helm.sh/docs/)
