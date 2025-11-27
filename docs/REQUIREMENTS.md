# Detailed Requirements Specification

This document outlines all functional and technical requirements gathered from stakeholder discussions.

## Functional Requirements

### 1. User Management

#### 1.1 Authentication
- **FR-1.1.1**: Users must register with email and password
- **FR-1.1.2**: Passwords must be hashed using bcrypt
- **FR-1.1.3**: Users must log in before accessing the panel
- **FR-1.1.4**: Sessions must expire after 7 days of inactivity
- **FR-1.1.5**: Password reset functionality via email (future)

#### 1.2 Authorization
- **FR-1.2.1**: System must support fine-grained permissions
- **FR-1.2.2**: Three permission scopes: Global, Server-level, Action-level
- **FR-1.2.3**: Global roles: Admin, User
- **FR-1.2.4**: Server-level roles: Owner, Sub-user
- **FR-1.2.5**: Action-level permissions:
  - View server details
  - Start/stop/restart server
  - Access console
  - Manage files
  - Edit server configuration
  - Delete server
  - Manage sub-users

#### 1.3 User Profile
- **FR-1.3.1**: Users can view their resource usage
- **FR-1.3.2**: Users can see their resource quota
- **FR-1.3.3**: Users can change their password
- **FR-1.3.4**: Users can see list of their servers

### 2. Server Management

#### 2.1 Server Creation
- **FR-2.1.1**: Users can create new Minecraft servers
- **FR-2.1.2**: Server creation requires:
  - Server name (unique per user)
  - Server type (Vanilla, Paper, Forge, etc.)
  - Server version (e.g., 1.20.1)
  - Resource plan (Small, Medium, Large) OR custom resources
- **FR-2.1.3**: System must validate resource quota before creation
- **FR-2.1.4**: System must download appropriate server JAR
- **FR-2.1.5**: Server must be created as Kubernetes StatefulSet
- **FR-2.1.6**: PersistentVolumeClaim must be provisioned for data

#### 2.2 Server Templates
- **FR-2.2.1**: Admins can create server templates (eggs)
- **FR-2.2.2**: Templates define:
  - Server type and version
  - Default configuration files
  - Startup command and parameters
  - Environment variables
  - Port mappings
  - Resource requirements
- **FR-2.2.3**: Users can create servers from templates
- **FR-2.2.4**: Templates include: Vanilla, Paper, Spigot, Forge, Fabric

#### 2.3 Server Control
- **FR-2.3.1**: Users can start a stopped server
- **FR-2.3.2**: Users can stop a running server
- **FR-2.3.3**: Users can restart a server
- **FR-2.3.4**: Users can force-kill a server (admin only)
- **FR-2.3.5**: System must track server status:
  - Creating
  - Starting
  - Running
  - Stopping
  - Stopped
  - Error

#### 2.4 Server Configuration
- **FR-2.4.1**: Users can edit server.properties
- **FR-2.4.2**: Users can modify JVM arguments
- **FR-2.4.3**: Users can change resource allocation (within quota)
- **FR-2.4.4**: Users can rename servers
- **FR-2.4.5**: Users can delete servers (with confirmation)

#### 2.5 Server Listing
- **FR-2.5.1**: Users see a dashboard with all their servers
- **FR-2.5.2**: Each server card shows:
  - Server name
  - Status (online/offline/starting)
  - Resource usage (CPU, RAM)
  - Player count (if running)
  - Quick action buttons
- **FR-2.5.3**: Admins can see all servers across all users

### 3. Console Access

#### 3.1 Live Console
- **FR-3.1.1**: Users can access a web-based terminal for their servers
- **FR-3.1.2**: Console must stream logs in real-time
- **FR-3.1.3**: Console must support ANSI color codes
- **FR-3.1.4**: Users can send commands via console
- **FR-3.1.5**: Console must show command history
- **FR-3.1.6**: Console must auto-scroll to latest output
- **FR-3.1.7**: Users can stop auto-scroll to review history

#### 3.2 Console Features
- **FR-3.2.1**: Command autocomplete for common Minecraft commands (future)
- **FR-3.2.2**: Search/filter console output (future)
- **FR-3.2.3**: Download console logs as file

### 4. File Management

#### 4.1 File Browser
- **FR-4.1.1**: Users can browse server files in web interface
- **FR-4.1.2**: File browser shows:
  - File/folder names
  - File sizes
  - Last modified dates
  - File icons based on type
- **FR-4.1.3**: Users can navigate directory structure
- **FR-4.1.4**: Users can upload files
- **FR-4.1.5**: Users can download files
- **FR-4.1.6**: Users can delete files/folders

#### 4.2 File Editor
- **FR-4.2.1**: Users can edit text files in browser
- **FR-4.2.2**: Editor must support syntax highlighting for:
  - YAML
  - JSON
  - Properties files
  - Java
- **FR-4.2.3**: Editor must have save/cancel buttons
- **FR-4.2.4**: Editor must warn before navigating away with unsaved changes

#### 4.3 File Operations
- **FR-4.3.1**: Users can create new files/folders
- **FR-4.3.2**: Users can rename files/folders
- **FR-4.3.3**: Users can copy files/folders
- **FR-4.3.4**: Users can move files/folders
- **FR-4.3.5**: Users can extract zip/tar archives
- **FR-4.3.6**: Users can compress files into archives

### 5. Resource Management

#### 5.1 Resource Plans
- **FR-5.1.1**: System defines predefined resource plans:
  - **Small**: 1 CPU core, 2Gi RAM, 10Gi disk
  - **Medium**: 2 CPU cores, 4Gi RAM, 20Gi disk
  - **Large**: 4 CPU cores, 8Gi RAM, 40Gi disk
- **FR-5.1.2**: Admins can create custom plans

#### 5.2 Custom Resources
- **FR-5.2.1**: Admins can set custom CPU/RAM per server
- **FR-5.2.2**: Custom resources must respect user quotas
- **FR-5.2.3**: System must validate resources are available

#### 5.3 Resource Quotas
- **FR-5.3.1**: Admins can set per-user resource quotas:
  - Maximum total CPU cores
  - Maximum total RAM
  - Maximum total disk space
  - Maximum number of servers
- **FR-5.3.2**: System must enforce quotas on server creation
- **FR-5.3.3**: System must prevent resource allocation beyond quota
- **FR-5.3.4**: Users can view their current quota usage

### 6. Sub-User Management

#### 6.1 Sub-User Access
- **FR-6.1.1**: Server owners can invite other users as sub-users
- **FR-6.1.2**: Sub-users have limited permissions on a server
- **FR-6.1.3**: Owners can grant/revoke specific permissions to sub-users:
  - Console access
  - File management
  - Start/stop server
  - Edit configuration
- **FR-6.1.4**: Owners can remove sub-users

### 7. Monitoring

#### 7.1 Server Monitoring
- **FR-7.1.1**: System must track server status (online/offline/starting)
- **FR-7.1.2**: System must collect resource usage:
  - CPU usage (percentage and absolute)
  - RAM usage (used/total)
  - Disk usage (used/total)
- **FR-7.1.3**: Dashboard displays resource usage in real-time
- **FR-7.1.4**: System must track player count when server is online

#### 7.2 Panel Monitoring
- **FR-7.2.1**: Prometheus scrapes metrics from Flask app
- **FR-7.2.2**: Grafana dashboards display:
  - API request rate
  - API error rate
  - API latency (p50, p95, p99)
  - Active user sessions
  - Database query performance
  - Server creation/deletion rate
- **FR-7.2.3**: Monitoring only for panel, not game servers

## Technical Requirements

### 8. Technology Stack

#### 8.1 Backend
- **TR-8.1.1**: Python 3.11+
- **TR-8.1.2**: Flask 3.0+
- **TR-8.1.3**: SQLAlchemy 2.0+ (ORM)
- **TR-8.1.4**: PostgreSQL 15+
- **TR-8.1.5**: Kubernetes Python client
- **TR-8.1.6**: Flask-SocketIO for WebSocket
- **TR-8.1.7**: Flask-Login for authentication

#### 8.2 Frontend
- **TR-8.2.1**: Jinja2 templates (server-side rendering)
- **TR-8.2.2**: Alpine.js for JavaScript interactivity
- **TR-8.2.3**: HTMX for AJAX interactions
- **TR-8.2.4**: Tailwind CSS for styling (or Bootstrap)

#### 8.3 Infrastructure
- **TR-8.3.1**: Kubernetes 1.28+
- **TR-8.3.2**: Helm 3.0+
- **TR-8.3.3**: Docker for containerization
- **TR-8.3.4**: GitHub Actions for CI/CD
- **TR-8.3.5**: ArgoCD for deployment
- **TR-8.3.6**: GitHub Container Registry (ghcr.io)

#### 8.4 Monitoring
- **TR-8.4.1**: Prometheus for metrics collection
- **TR-8.4.2**: Grafana for visualization

### 9. Deployment

#### 9.1 Containerization
- **TR-9.1.1**: Flask app packaged as Docker image
- **TR-9.1.2**: Multi-stage build for smaller images
- **TR-9.1.3**: Non-root user in container
- **TR-9.1.4**: Health checks configured

#### 9.2 Helm Chart
- **TR-9.2.1**: Helm chart includes:
  - Flask Deployment
  - PostgreSQL StatefulSet
  - Services
  - ConfigMaps
  - Secrets
  - RBAC (ServiceAccount, Role, RoleBinding)
  - NetworkPolicies
- **TR-9.2.2**: Configurable via values.yaml:
  - Image tag
  - Resource limits
  - Replica count
  - Database credentials
  - Environment variables

#### 9.3 CI/CD Pipeline
- **TR-9.3.1**: GitHub Actions workflow triggers on push to main
- **TR-9.3.2**: Pipeline stages:
  1. Lint (black, flake8, mypy)
  2. Unit tests (pytest)
  3. Build Docker image
  4. Push to ghcr.io
  5. Update Helm chart version
- **TR-9.3.3**: ArgoCD watches Git repository
- **TR-9.3.4**: ArgoCD deploys on chart changes

#### 9.4 Target Environment
- **TR-9.4.1**: Self-hosted on-premises Kubernetes cluster
- **TR-9.4.2**: ClusterIP service for panel (internal access only)
- **TR-9.4.3**: ClusterIP service for game servers (for now)

### 10. Security

#### 10.1 Authentication & Authorization
- **TR-10.1.1**: Password hashing with bcrypt (cost factor 12)
- **TR-10.1.2**: Session tokens stored in database
- **TR-10.1.3**: CSRF protection on all forms
- **TR-10.1.4**: Permission checks on every API endpoint

#### 10.2 Kubernetes Security
- **TR-10.2.1**: ServiceAccount with minimal RBAC permissions
- **TR-10.2.2**: Network policies to isolate game servers
- **TR-10.2.3**: Pod security standards enforced
- **TR-10.2.4**: Secrets stored in Kubernetes Secrets (not hardcoded)

#### 10.3 Application Security
- **TR-10.3.1**: Input validation on all user inputs
- **TR-10.3.2**: SQL injection prevention via ORM
- **TR-10.3.3**: XSS prevention via template auto-escaping
- **TR-10.3.4**: Rate limiting on API endpoints
- **TR-10.3.5**: Secure headers (CSP, HSTS, etc.)

### 11. Performance

#### 11.1 Scalability
- **TR-11.1.1**: Flask app stateless for horizontal scaling
- **TR-11.1.2**: Database connection pooling
- **TR-11.1.3**: Redis caching for frequently accessed data (future)

#### 11.2 Efficiency
- **TR-11.2.1**: API response time < 200ms (p95)
- **TR-11.2.2**: Console log streaming < 100ms latency
- **TR-11.2.3**: File browser loads < 500ms

### 12. Data Persistence

#### 12.1 Database
- **TR-12.1.1**: PostgreSQL data stored in PVC
- **TR-12.1.2**: Database backups daily via CronJob
- **TR-12.1.3**: Backup retention: 7 days

#### 12.2 Game Server Data
- **TR-12.2.1**: Each server gets dedicated PVC
- **TR-12.2.2**: PVCs survive pod deletion
- **TR-12.2.3**: PVC size based on resource plan

## Non-Functional Requirements

### 13. Usability
- **NFR-13.1**: Dashboard must be intuitive for non-technical users
- **NFR-13.2**: All actions must provide user feedback (success/error messages)
- **NFR-13.3**: Loading states for async operations

### 14. Reliability
- **NFR-14.1**: Panel uptime > 99%
- **NFR-14.2**: Graceful handling of Kubernetes API failures
- **NFR-14.3**: Automatic restart of crashed game servers

### 15. Maintainability
- **NFR-15.1**: Code coverage > 80%
- **NFR-15.2**: All code passes linting (black, flake8)
- **NFR-15.3**: Type hints on all functions
- **NFR-15.4**: Comprehensive documentation

### 16. Observability
- **NFR-16.1**: All errors logged with context
- **NFR-16.2**: Audit log for user actions
- **NFR-16.3**: Prometheus metrics for key operations
