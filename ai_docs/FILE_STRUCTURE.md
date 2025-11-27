# Complete File Structure

This document shows the exact file structure for the entire project. Use this as a reference when creating files.

```
server-panel/
│
├── .github/
│   └── workflows/
│       ├── ci.yml                    # Linting and testing workflow
│       ├── build.yml                 # Docker build and push workflow
│       └── release.yml               # Helm chart release workflow
│
├── app/                              # Main Flask application
│   ├── __init__.py                   # App factory, blueprint registration
│   ├── config.py                     # Configuration classes
│   ├── models.py                     # Database models (User, Server, etc.)
│   │
│   ├── auth/                         # Authentication blueprint
│   │   ├── __init__.py
│   │   ├── routes.py                 # Login, register, logout routes
│   │   └── forms.py                  # WTForms for auth (optional)
│   │
│   ├── servers/                      # Server management blueprint
│   │   ├── __init__.py
│   │   ├── routes.py                 # Server CRUD, dashboard
│   │   ├── kubernetes_client.py      # K8s API wrapper
│   │   └── resource_manager.py       # Resource quota calculations
│   │
│   ├── console/                      # Console blueprint
│   │   ├── __init__.py
│   │   ├── routes.py                 # WebSocket handlers
│   │   └── log_streamer.py           # Kubernetes log streaming
│   │
│   ├── files/                        # File manager blueprint
│   │   ├── __init__.py
│   │   ├── routes.py                 # File browser, editor endpoints
│   │   └── file_operations.py        # File CRUD via kubectl exec
│   │
│   ├── api/                          # REST API blueprint
│   │   ├── __init__.py
│   │   ├── routes.py                 # API endpoints
│   │   └── serializers.py            # Response formatters
│   │
│   ├── templates/                    # Jinja2 templates
│   │   ├── base.html                 # Base layout
│   │   ├── index.html                # Landing page
│   │   │
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   │
│   │   ├── servers/
│   │   │   ├── dashboard.html        # Main dashboard
│   │   │   ├── create.html           # Server creation form
│   │   │   ├── detail.html           # Server details page
│   │   │   └── components/
│   │   │       ├── server_card.html  # Reusable server card
│   │   │       └── resource_meter.html
│   │   │
│   │   ├── console/
│   │   │   └── console.html          # Terminal interface
│   │   │
│   │   └── files/
│   │       ├── browser.html          # File browser
│   │       └── editor.html           # File editor
│   │
│   ├── static/                       # Static assets
│   │   ├── css/
│   │   │   ├── main.css              # Custom styles
│   │   │   └── terminal.css          # Console styling
│   │   │
│   │   ├── js/
│   │   │   ├── console.js            # WebSocket console client
│   │   │   ├── file-browser.js       # File manager JavaScript
│   │   │   └── dashboard.js          # Dashboard interactivity
│   │   │
│   │   └── images/
│   │       ├── logo.png
│   │       └── icons/
│   │
│   └── utils/                        # Utility functions
│       ├── __init__.py
│       ├── decorators.py             # Custom decorators (permission checks)
│       └── validators.py             # Input validation
│
├── helm/                             # Helm chart
│   └── server-panel/
│       ├── Chart.yaml                # Chart metadata
│       ├── values.yaml               # Default configuration values
│       ├── values-dev.yaml           # Development overrides
│       ├── values-prod.yaml          # Production overrides
│       │
│       └── templates/
│           ├── NOTES.txt             # Post-install notes
│           ├── _helpers.tpl          # Template helpers
│           │
│           ├── deployment.yaml       # Flask app Deployment
│           ├── service.yaml          # Flask app Service
│           ├── configmap.yaml        # Configuration
│           ├── secret.yaml           # Sensitive data
│           │
│           ├── postgresql/
│           │   ├── statefulset.yaml  # PostgreSQL StatefulSet
│           │   ├── service.yaml      # PostgreSQL Service
│           │   └── pvc.yaml          # Database PVC
│           │
│           ├── rbac/
│           │   ├── serviceaccount.yaml
│           │   ├── role.yaml         # Permissions for managing game servers
│           │   └── rolebinding.yaml
│           │
│           └── monitoring/
│               └── servicemonitor.yaml  # Prometheus ServiceMonitor
│
├── tests/                            # Test suite
│   ├── __init__.py
│   ├── conftest.py                   # Pytest fixtures
│   │
│   ├── unit/
│   │   ├── test_models.py            # Database model tests
│   │   ├── test_auth.py              # Authentication tests
│   │   ├── test_kubernetes_client.py # K8s client tests (mocked)
│   │   └── test_validators.py
│   │
│   ├── integration/
│   │   ├── test_server_creation.py   # Full server creation flow
│   │   ├── test_console.py           # Console functionality
│   │   └── test_file_operations.py
│   │
│   └── fixtures/
│       ├── mock_k8s_responses.py     # Mock Kubernetes API responses
│       └── sample_data.py            # Test data
│
├── docs/                             # User documentation
│   ├── PROJECT_OVERVIEW.md
│   ├── ARCHITECTURE.md
│   ├── REQUIREMENTS.md
│   ├── GLOSSARY.md
│   ├── API.md                        # API documentation
│   ├── DEPLOYMENT.md                 # Deployment guide
│   └── USER_GUIDE.md                 # End-user instructions
│
├── ai_docs/                          # AI-specific documentation
│   ├── AI_CHECKLIST.md               # This file you're reading
│   ├── FILE_STRUCTURE.md             # Directory structure
│   ├── IMPLEMENTATION_GUIDE.md       # Code patterns and examples
│   ├── TESTING_GUIDE.md              # Testing instructions
│   └── COMMON_PITFALLS.md            # Things to avoid
│
├── scripts/                          # Helper scripts
│   ├── setup_dev.sh                  # Development environment setup
│   ├── create_admin.py               # Create admin user
│   └── seed_templates.py             # Seed server templates
│
├── migrations/                       # Database migrations (if using Flask-Migrate)
│   └── versions/
│
├── .gitignore                        # Git ignore rules
├── .dockerignore                     # Docker ignore rules
├── Dockerfile                        # Container image definition
├── docker-compose.yml                # Local development with Docker Compose
├── requirements.txt                  # Python dependencies
├── requirements-dev.txt              # Development dependencies
├── setup.py                          # Package setup (optional)
├── pytest.ini                        # Pytest configuration
├── .flake8                           # Flake8 linter config
├── pyproject.toml                    # Black formatter config
├── mypy.ini                          # Type checker config
├── README.md                         # Project README
├── LICENSE                           # License file
└── run.py                            # Application entry point
```

## Directory Purposes

### `/app`
Core Flask application. All Python backend code lives here.

### `/app/templates`
Jinja2 HTML templates. Organized by blueprint/feature.

### `/app/static`
CSS, JavaScript, images. Served directly by Flask in development.

### `/helm`
Kubernetes deployment manifests packaged as a Helm chart.

### `/tests`
All test code. Separated into unit and integration tests.

### `/docs`
User-facing documentation for understanding and using the system.

### `/ai_docs`
AI-specific documentation for implementation guidance.

### `/scripts`
Utility scripts for setup, database seeding, etc.

## File Naming Conventions

- **Python files**: `snake_case.py`
- **Templates**: `lowercase.html`
- **CSS/JS**: `kebab-case.css`, `kebab-case.js`
- **Config files**: `lowercase.yml`, `UPPERCASE.md` (for important docs)

## Import Conventions

- Always use absolute imports from `app`:
  ```python
  from app.models import User, Server
  from app.servers.kubernetes_client import KubernetesClient
  ```

- Never use relative imports:
  ```python
  from ..models import User  # DON'T DO THIS
  ```

## Blueprint Organization

Each blueprint follows this pattern:
```
blueprint_name/
├── __init__.py         # Create and export blueprint
├── routes.py           # View functions and API endpoints
└── [helper_module].py  # Business logic, separate from routes
```

This keeps route handlers thin and testable.
