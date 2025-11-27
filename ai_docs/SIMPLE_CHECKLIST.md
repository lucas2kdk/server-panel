# Simple AI Checklist - No Code, Just Tasks

A streamlined checklist for implementing the Kubernetes Game Server Panel. Each item is a discrete task that can be checked off.

## Setup & Initialization

- [x] Create project root directory `server-panel/`
- [x] Initialize git repository
- [x] Create `.gitignore` file
- [x] Create `README.md` with project description
- [x] Create Python virtual environment
- [x] Create `requirements.txt` with all dependencies
- [x] Create `requirements-dev.txt` with testing/linting dependencies
- [x] Install all Python packages
- [x] Create directory structure: `app/`, `helm/`, `.github/workflows/`, `tests/`, `docs/`

## Flask Application Structure

- [x] Create `app/__init__.py` - Flask app factory
- [x] Create `app/config.py` - Configuration classes (Development, Production)
- [x] Create `app/models.py` - Database models
- [x] Add User model with authentication fields
- [x] Add Server model with Kubernetes and resource fields
- [x] Add ServerPermission model for fine-grained access
- [x] Add ServerTemplate model for server templates/eggs
- [x] Add AuditLog model for tracking actions
- [x] Create `run.py` - Application entry point

## Authentication Blueprint

- [x] Create `app/auth/` directory
- [x] Create `app/auth/__init__.py` - Define auth blueprint
- [x] Create `app/auth/routes.py` - Login, register, logout routes
- [ ] Implement password hashing with bcrypt
- [x] Set up Flask-Login user session management
- [x] Create `app/templates/auth/login.html`
- [x] Create `app/templates/auth/register.html`
- [x] Create `app/templates/base.html` - Base template with navigation

## Server Management Blueprint

- [x] Create `app/servers/` directory
- [x] Create `app/servers/__init__.py` - Define servers blueprint
- [x] Create `app/servers/routes.py` - Server CRUD routes
- [x] Create dashboard route showing all user servers
- [x] Create server creation route with form
- [x] Create server detail/view route
- [x] Create server start route
- [x] Create server stop route
- [x] Create server restart route
- [x] Create server delete route
- [x] Create `app/templates/servers/dashboard.html`
- [x] Create `app/templates/servers/create.html`
- [x] Create `app/templates/servers/detail.html`

## Kubernetes Integration

- [x] Create `app/servers/kubernetes_client.py`
- [x] Implement Kubernetes client initialization (in-cluster vs local)
- [x] Implement PersistentVolumeClaim creation method
- [x] Implement StatefulSet creation method for Minecraft servers
- [x] Implement Service creation method
- [x] Implement server deletion method (delete StatefulSet, PVC, Service)
- [x] Implement get server status method
- [x] Implement start server method (scale to 1)
- [x] Implement stop server method (scale to 0)
- [x] Implement get server logs method
- [x] Implement exec command in pod method
- [x] Add error handling for Kubernetes API failures

## Resource Management

- [ ] Create `app/servers/resource_manager.py`
- [ ] Implement resource quota checking logic
- [ ] Define resource plans (Small, Medium, Large)
- [ ] Implement method to calculate user's current resource usage
- [ ] Implement method to check if user can create server
- [ ] Add validation before server creation

## Console Blueprint

- [x] Create `app/console/` directory
- [x] Create `app/console/__init__.py` - Define console blueprint
- [x] Create `app/console/routes.py` - Console view and WebSocket handlers
- [ ] Install and configure Flask-SocketIO
- [ ] Implement WebSocket connect handler with authentication
- [ ] Implement join room handler for specific server
- [ ] Implement log streaming from Kubernetes to WebSocket
- [ ] Implement command execution handler
- [ ] Implement disconnect handler
- [x] Create `app/templates/console/console.html` - Terminal UI
- [ ] Create `app/static/js/console.js` - WebSocket client JavaScript
- [ ] Add ANSI color code support in terminal display

## File Manager Blueprint

- [x] Create `app/files/` directory
- [x] Create `app/files/__init__.py` - Define files blueprint
- [x] Create `app/files/routes.py` - File operations routes
- [x] Implement file listing route (execute ls in pod)
- [x] Implement file read route (execute cat in pod)
- [x] Implement file write route (execute tee/echo in pod)
- [ ] Implement file delete route
- [ ] Implement file upload route
- [ ] Implement file download route
- [x] Create `app/templates/files/browser.html` - File browser UI
- [ ] Create `app/templates/files/editor.html` - File editor with syntax highlighting
- [ ] Create `app/static/js/file-browser.js` - File manager JavaScript

## Permission System

- [ ] Create `app/utils/decorators.py`
- [ ] Implement permission checking decorator
- [ ] Add sub-user invitation route
- [ ] Add sub-user management route
- [ ] Add permission grant/revoke route
- [ ] Apply permission checks to all server routes
- [ ] Test that sub-users can only access granted permissions

## Server Templates (Eggs)

- [ ] Create admin route to create server templates
- [ ] Create admin route to edit server templates
- [ ] Create admin route to delete server templates
- [ ] Modify server creation to support template selection
- [ ] Create seed script to add default templates (Vanilla, Paper, Forge, etc.)
- [ ] Create `app/templates/servers/templates.html` - Template management UI

## API Blueprint (Optional)

- [x] Create `app/api/` directory
- [x] Create `app/api/__init__.py` - Define API blueprint
- [x] Create `app/api/routes.py` - RESTful API endpoints
- [ ] Implement API authentication (token-based)
- [x] Implement GET /api/servers - List servers
- [ ] Implement POST /api/servers - Create server
- [x] Implement GET /api/servers/:id - Get server details
- [ ] Implement DELETE /api/servers/:id - Delete server
- [ ] Implement POST /api/servers/:id/start - Start server
- [ ] Implement POST /api/servers/:id/stop - Stop server
- [ ] Add API documentation

## Frontend Polish

- [x] Add Tailwind CSS for styling
- [x] Add Alpine.js for JavaScript interactivity
- [x] Add HTMX for AJAX interactions
- [x] Create responsive navigation bar
- [ ] Add loading spinners for async operations
- [x] Add success/error flash messages
- [x] Create server status badges (running, stopped, error)
- [x] Add resource usage meters/progress bars
- [ ] Make dashboard auto-refresh server statuses

## Docker & Containerization

- [x] Create `Dockerfile` for Flask application
- [x] Use multi-stage build to reduce image size
- [x] Configure non-root user in container
- [x] Add health check endpoint in Flask
- [x] Add health check in Dockerfile
- [x] Create `.dockerignore` file
- [ ] Test local Docker build
- [ ] Test running container locally
- [x] Create `docker-compose.yml` for local development

## Helm Chart - Structure

- [x] Create `helm/server-panel/` directory
- [x] Create `Chart.yaml` with metadata
- [x] Create `values.yaml` with default configuration
- [x] Create `values-dev.yaml` for development overrides
- [x] Create `values-prod.yaml` for production overrides
- [x] Create `templates/` directory
- [x] Create `templates/_helpers.tpl` for template helpers
- [x] Create `templates/NOTES.txt` for post-install instructions

## Helm Chart - Panel Resources

- [x] Create `templates/deployment.yaml` - Flask app Deployment
- [x] Create `templates/service.yaml` - Flask app Service (ClusterIP)
- [x] Create `templates/configmap.yaml` - Configuration values
- [x] Create `templates/secret.yaml` - Database credentials, secret key
- [x] Configure resource limits/requests in Deployment
- [x] Configure liveness and readiness probes
- [x] Add pod labels and selectors

## Helm Chart - Database

- [x] Create `templates/postgresql/statefulset.yaml` - PostgreSQL StatefulSet
- [x] Create `templates/postgresql/service.yaml` - PostgreSQL Service
- [x] Create `templates/postgresql/pvc.yaml` - PostgreSQL PVC
- [x] Configure PostgreSQL environment variables
- [ ] Add PostgreSQL init scripts if needed

## Helm Chart - RBAC

- [x] Create `templates/rbac/serviceaccount.yaml`
- [x] Create `templates/rbac/role.yaml` with permissions to:
  - Create/delete StatefulSets
  - Create/delete PVCs
  - Create/delete Services
  - Get/list/watch Pods
  - Exec into Pods
  - Read Pod logs
- [x] Create `templates/rbac/rolebinding.yaml`
- [x] Bind ServiceAccount to Deployment
- [ ] Test RBAC permissions work

## Helm Chart - Monitoring

- [x] Create `templates/monitoring/servicemonitor.yaml` for Prometheus
- [x] Configure Prometheus scraping endpoint
- [ ] Test Prometheus can scrape metrics

## Helm Chart - Testing

- [ ] Run `helm lint helm/server-panel` to check for errors
- [ ] Run `helm template helm/server-panel` to render templates
- [ ] Test install on local cluster: `helm install test helm/server-panel`
- [ ] Verify all resources created correctly
- [ ] Test upgrade: `helm upgrade test helm/server-panel`
- [ ] Test rollback: `helm rollback test`
- [ ] Test uninstall: `helm uninstall test`

## GitHub Actions - CI Workflow

- [x] Create `.github/workflows/ci.yml`
- [x] Add job to run Black formatter check
- [x] Add job to run Flake8 linter
- [x] Add job to run mypy type checker
- [x] Add job to run pytest unit tests
- [x] Add job to check test coverage
- [x] Configure workflow to run on push and pull request
- [x] Add status badge to README

## GitHub Actions - Build Workflow

- [x] Create `.github/workflows/build.yml`
- [x] Add job to build Docker image
- [x] Add job to tag image with commit SHA and 'latest'
- [x] Add job to push image to ghcr.io (GitHub Container Registry)
- [x] Configure GitHub secrets for registry authentication
- [x] Test workflow triggers on push to main branch
- [x] Verify image appears in GitHub Packages

## GitHub Actions - Release Workflow (Optional)

- [x] Create `.github/workflows/release.yml`
- [x] Add job to package Helm chart
- [x] Add job to update Helm chart version
- [x] Add job to publish Helm chart to registry
- [x] Configure workflow to run on tag creation

## ArgoCD Setup

- [ ] Create ArgoCD Application manifest
- [ ] Configure Git repository source
- [ ] Configure target Kubernetes cluster and namespace
- [ ] Set sync policy (manual or automatic)
- [ ] Apply ArgoCD Application to cluster
- [ ] Test that ArgoCD detects Helm chart
- [ ] Test manual sync
- [ ] Test automatic sync on Git push

## Monitoring & Observability

- [ ] Install prometheus-flask-exporter in Flask app
- [ ] Add /metrics endpoint
- [ ] Add custom metrics for server creation/deletion
- [ ] Add custom metrics for active servers count
- [ ] Deploy Prometheus to cluster
- [ ] Configure Prometheus to scrape panel metrics
- [ ] Deploy Grafana to cluster
- [ ] Create Grafana dashboard for panel metrics
- [ ] Import dashboard to Grafana
- [ ] Test metrics are visible

## Testing - Unit Tests

- [x] Create `tests/unit/` directory
- [x] Create `tests/conftest.py` with pytest fixtures
- [x] Write tests for User model methods
- [x] Write tests for Server model methods
- [x] Write tests for authentication routes
- [ ] Write tests for resource quota checking
- [ ] Write tests for permission decorators
- [x] Configure pytest in `pytest.ini`
- [ ] Run all unit tests and ensure they pass

## Testing - Integration Tests

- [x] Create `tests/integration/` directory
- [ ] Write test for complete server creation flow
- [ ] Write test for server start/stop
- [ ] Write test for console connection
- [ ] Write test for file operations
- [ ] Mock Kubernetes API responses
- [ ] Run all integration tests and ensure they pass

## Security Hardening

- [ ] Ensure all passwords are hashed with bcrypt
- [ ] Add CSRF protection to all forms
- [ ] Add rate limiting to API endpoints
- [ ] Add input validation on all user inputs
- [ ] Sanitize file paths in file manager
- [x] Ensure SQL injection prevention via ORM
- [ ] Add secure HTTP headers (CSP, HSTS, X-Frame-Options)
- [ ] Review Kubernetes RBAC permissions (principle of least privilege)
- [ ] Store secrets in Kubernetes Secrets, not in code
- [ ] Test for common vulnerabilities (XSS, CSRF, SQL injection)

## Documentation

- [x] Update README.md with:
  - Project description
  - Features list
  - Screenshots (optional)
  - Installation instructions
  - Development setup guide
  - Deployment guide
  - License
- [ ] Create `docs/API.md` - API endpoint documentation
- [ ] Create `docs/DEPLOYMENT.md` - Production deployment guide
- [ ] Create `docs/USER_GUIDE.md` - End-user instructions
- [ ] Create `docs/DEVELOPMENT.md` - Developer setup guide
- [ ] Create `docs/TROUBLESHOOTING.md` - Common issues and solutions
- [ ] Add code comments to complex functions
- [x] Add docstrings to all functions and classes

## Deployment & Validation

- [ ] Deploy to self-hosted Kubernetes cluster
- [ ] Verify all pods are running
- [ ] Create admin user account
- [ ] Create test user account
- [ ] Create test Minecraft server
- [ ] Verify server pod is created in Kubernetes
- [ ] Verify PVC is created and bound
- [ ] Connect to server console
- [ ] Send command and verify output
- [ ] Browse server files
- [ ] Edit a file and save
- [ ] Stop server and verify pod scales down
- [ ] Start server and verify pod scales up
- [ ] Delete server and verify resources are cleaned up
- [ ] Test sub-user permissions
- [ ] Monitor metrics in Grafana
- [ ] Review logs for errors

## Polish & Optimization

- [ ] Add database connection pooling
- [ ] Add Redis caching for frequently accessed data (optional)
- [ ] Optimize database queries (add indexes)
- [ ] Add database migrations support (Flask-Migrate)
- [ ] Add pagination to server list
- [ ] Add search/filter for servers
- [ ] Add sorting options
- [ ] Add user profile page
- [ ] Add ability to change password
- [ ] Add email verification (optional)
- [ ] Add forgot password functionality (optional)
- [ ] Add audit log viewer for admins

## Future Enhancements (Phase 2+)

- [ ] Add scheduled tasks (backups, restarts, commands)
- [ ] Add server backup functionality
- [ ] Add server restoration from backup
- [ ] Support for additional game types (Terraria, Valheim, etc.)
- [ ] OAuth2 authentication (Google, GitHub, Discord)
- [ ] LDAP/Active Directory integration
- [ ] Multi-cluster support
- [ ] Server auto-scaling based on player count
- [ ] Player whitelist management
- [ ] Plugin/mod manager
- [ ] Server performance graphs
- [ ] Email notifications for server events

---

## Quick Verification Commands

After each major section, use these to verify:

```bash
# Check syntax
python -m py_compile app/file.py

# Run tests
pytest

# Lint code
black app/ --check
flake8 app/

# Build Docker image
docker build -t server-panel .

# Lint Helm chart
helm lint helm/server-panel

# Render Helm templates
helm template helm/server-panel

# Check Kubernetes pods
kubectl get pods -n game-servers
```
