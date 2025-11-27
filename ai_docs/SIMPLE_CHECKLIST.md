# Simple AI Checklist - No Code, Just Tasks

A streamlined checklist for implementing the Kubernetes Game Server Panel. Each item is a discrete task that can be checked off.

## Setup & Initialization

- [ ] Create project root directory `server-panel/`
- [ ] Initialize git repository
- [ ] Create `.gitignore` file
- [ ] Create `README.md` with project description
- [ ] Create Python virtual environment
- [ ] Create `requirements.txt` with all dependencies
- [ ] Create `requirements-dev.txt` with testing/linting dependencies
- [ ] Install all Python packages
- [ ] Create directory structure: `app/`, `helm/`, `.github/workflows/`, `tests/`, `docs/`

## Flask Application Structure

- [ ] Create `app/__init__.py` - Flask app factory
- [ ] Create `app/config.py` - Configuration classes (Development, Production)
- [ ] Create `app/models.py` - Database models
- [ ] Add User model with authentication fields
- [ ] Add Server model with Kubernetes and resource fields
- [ ] Add ServerPermission model for fine-grained access
- [ ] Add ServerTemplate model for server templates/eggs
- [ ] Add AuditLog model for tracking actions
- [ ] Create `run.py` - Application entry point

## Authentication Blueprint

- [ ] Create `app/auth/` directory
- [ ] Create `app/auth/__init__.py` - Define auth blueprint
- [ ] Create `app/auth/routes.py` - Login, register, logout routes
- [ ] Implement password hashing with bcrypt
- [ ] Set up Flask-Login user session management
- [ ] Create `app/templates/auth/login.html`
- [ ] Create `app/templates/auth/register.html`
- [ ] Create `app/templates/base.html` - Base template with navigation

## Server Management Blueprint

- [ ] Create `app/servers/` directory
- [ ] Create `app/servers/__init__.py` - Define servers blueprint
- [ ] Create `app/servers/routes.py` - Server CRUD routes
- [ ] Create dashboard route showing all user servers
- [ ] Create server creation route with form
- [ ] Create server detail/view route
- [ ] Create server start route
- [ ] Create server stop route
- [ ] Create server restart route
- [ ] Create server delete route
- [ ] Create `app/templates/servers/dashboard.html`
- [ ] Create `app/templates/servers/create.html`
- [ ] Create `app/templates/servers/detail.html`

## Kubernetes Integration

- [ ] Create `app/servers/kubernetes_client.py`
- [ ] Implement Kubernetes client initialization (in-cluster vs local)
- [ ] Implement PersistentVolumeClaim creation method
- [ ] Implement StatefulSet creation method for Minecraft servers
- [ ] Implement Service creation method
- [ ] Implement server deletion method (delete StatefulSet, PVC, Service)
- [ ] Implement get server status method
- [ ] Implement start server method (scale to 1)
- [ ] Implement stop server method (scale to 0)
- [ ] Implement get server logs method
- [ ] Implement exec command in pod method
- [ ] Add error handling for Kubernetes API failures

## Resource Management

- [ ] Create `app/servers/resource_manager.py`
- [ ] Implement resource quota checking logic
- [ ] Define resource plans (Small, Medium, Large)
- [ ] Implement method to calculate user's current resource usage
- [ ] Implement method to check if user can create server
- [ ] Add validation before server creation

## Console Blueprint

- [ ] Create `app/console/` directory
- [ ] Create `app/console/__init__.py` - Define console blueprint
- [ ] Create `app/console/routes.py` - Console view and WebSocket handlers
- [ ] Install and configure Flask-SocketIO
- [ ] Implement WebSocket connect handler with authentication
- [ ] Implement join room handler for specific server
- [ ] Implement log streaming from Kubernetes to WebSocket
- [ ] Implement command execution handler
- [ ] Implement disconnect handler
- [ ] Create `app/templates/console/console.html` - Terminal UI
- [ ] Create `app/static/js/console.js` - WebSocket client JavaScript
- [ ] Add ANSI color code support in terminal display

## File Manager Blueprint

- [ ] Create `app/files/` directory
- [ ] Create `app/files/__init__.py` - Define files blueprint
- [ ] Create `app/files/routes.py` - File operations routes
- [ ] Implement file listing route (execute ls in pod)
- [ ] Implement file read route (execute cat in pod)
- [ ] Implement file write route (execute tee/echo in pod)
- [ ] Implement file delete route
- [ ] Implement file upload route
- [ ] Implement file download route
- [ ] Create `app/templates/files/browser.html` - File browser UI
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

- [ ] Create `app/api/` directory
- [ ] Create `app/api/__init__.py` - Define API blueprint
- [ ] Create `app/api/routes.py` - RESTful API endpoints
- [ ] Implement API authentication (token-based)
- [ ] Implement GET /api/servers - List servers
- [ ] Implement POST /api/servers - Create server
- [ ] Implement GET /api/servers/:id - Get server details
- [ ] Implement DELETE /api/servers/:id - Delete server
- [ ] Implement POST /api/servers/:id/start - Start server
- [ ] Implement POST /api/servers/:id/stop - Stop server
- [ ] Add API documentation

## Frontend Polish

- [ ] Add Tailwind CSS for styling
- [ ] Add Alpine.js for JavaScript interactivity
- [ ] Add HTMX for AJAX interactions
- [ ] Create responsive navigation bar
- [ ] Add loading spinners for async operations
- [ ] Add success/error flash messages
- [ ] Create server status badges (running, stopped, error)
- [ ] Add resource usage meters/progress bars
- [ ] Make dashboard auto-refresh server statuses

## Docker & Containerization

- [ ] Create `Dockerfile` for Flask application
- [ ] Use multi-stage build to reduce image size
- [ ] Configure non-root user in container
- [ ] Add health check endpoint in Flask
- [ ] Add health check in Dockerfile
- [ ] Create `.dockerignore` file
- [ ] Test local Docker build
- [ ] Test running container locally
- [ ] Create `docker-compose.yml` for local development

## Helm Chart - Structure

- [ ] Create `helm/server-panel/` directory
- [ ] Create `Chart.yaml` with metadata
- [ ] Create `values.yaml` with default configuration
- [ ] Create `values-dev.yaml` for development overrides
- [ ] Create `values-prod.yaml` for production overrides
- [ ] Create `templates/` directory
- [ ] Create `templates/_helpers.tpl` for template helpers
- [ ] Create `templates/NOTES.txt` for post-install instructions

## Helm Chart - Panel Resources

- [ ] Create `templates/deployment.yaml` - Flask app Deployment
- [ ] Create `templates/service.yaml` - Flask app Service (ClusterIP)
- [ ] Create `templates/configmap.yaml` - Configuration values
- [ ] Create `templates/secret.yaml` - Database credentials, secret key
- [ ] Configure resource limits/requests in Deployment
- [ ] Configure liveness and readiness probes
- [ ] Add pod labels and selectors

## Helm Chart - Database

- [ ] Create `templates/postgresql/statefulset.yaml` - PostgreSQL StatefulSet
- [ ] Create `templates/postgresql/service.yaml` - PostgreSQL Service
- [ ] Create `templates/postgresql/pvc.yaml` - PostgreSQL PVC
- [ ] Configure PostgreSQL environment variables
- [ ] Add PostgreSQL init scripts if needed

## Helm Chart - RBAC

- [ ] Create `templates/rbac/serviceaccount.yaml`
- [ ] Create `templates/rbac/role.yaml` with permissions to:
  - Create/delete StatefulSets
  - Create/delete PVCs
  - Create/delete Services
  - Get/list/watch Pods
  - Exec into Pods
  - Read Pod logs
- [ ] Create `templates/rbac/rolebinding.yaml`
- [ ] Bind ServiceAccount to Deployment
- [ ] Test RBAC permissions work

## Helm Chart - Monitoring

- [ ] Create `templates/monitoring/servicemonitor.yaml` for Prometheus
- [ ] Configure Prometheus scraping endpoint
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

- [ ] Create `.github/workflows/ci.yml`
- [ ] Add job to run Black formatter check
- [ ] Add job to run Flake8 linter
- [ ] Add job to run mypy type checker
- [ ] Add job to run pytest unit tests
- [ ] Add job to check test coverage
- [ ] Configure workflow to run on push and pull request
- [ ] Add status badge to README

## GitHub Actions - Build Workflow

- [ ] Create `.github/workflows/build.yml`
- [ ] Add job to build Docker image
- [ ] Add job to tag image with commit SHA and 'latest'
- [ ] Add job to push image to ghcr.io (GitHub Container Registry)
- [ ] Configure GitHub secrets for registry authentication
- [ ] Test workflow triggers on push to main branch
- [ ] Verify image appears in GitHub Packages

## GitHub Actions - Release Workflow (Optional)

- [ ] Create `.github/workflows/release.yml`
- [ ] Add job to package Helm chart
- [ ] Add job to update Helm chart version
- [ ] Add job to publish Helm chart to registry
- [ ] Configure workflow to run on tag creation

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

- [ ] Create `tests/unit/` directory
- [ ] Create `tests/conftest.py` with pytest fixtures
- [ ] Write tests for User model methods
- [ ] Write tests for Server model methods
- [ ] Write tests for authentication routes
- [ ] Write tests for resource quota checking
- [ ] Write tests for permission decorators
- [ ] Configure pytest in `pytest.ini`
- [ ] Run all unit tests and ensure they pass

## Testing - Integration Tests

- [ ] Create `tests/integration/` directory
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
- [ ] Ensure SQL injection prevention via ORM
- [ ] Add secure HTTP headers (CSP, HSTS, X-Frame-Options)
- [ ] Review Kubernetes RBAC permissions (principle of least privilege)
- [ ] Store secrets in Kubernetes Secrets, not in code
- [ ] Test for common vulnerabilities (XSS, CSRF, SQL injection)

## Documentation

- [ ] Update README.md with:
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
- [ ] Add docstrings to all functions and classes

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
