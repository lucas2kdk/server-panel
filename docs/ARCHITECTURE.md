# System Architecture

## Overview

The panel follows a microservices-inspired architecture running entirely within Kubernetes, with the Flask application as the control plane for managing game server pods.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Kubernetes Cluster                        │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │              Panel Namespace                        │    │
│  │                                                     │    │
│  │  ┌──────────────┐      ┌──────────────┐           │    │
│  │  │   Flask App  │──────│  PostgreSQL  │           │    │
│  │  │  (ClusterIP) │      │   Database   │           │    │
│  │  └──────┬───────┘      └──────────────┘           │    │
│  │         │                                          │    │
│  │         │ K8s API                                  │    │
│  │         │                                          │    │
│  └─────────┼──────────────────────────────────────────┘    │
│            │                                               │
│  ┌─────────▼──────────────────────────────────────────┐    │
│  │         Game Servers Namespace                     │    │
│  │                                                     │    │
│  │  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │  Minecraft   │  │  Minecraft   │   ...        │    │
│  │  │  Server 1    │  │  Server 2    │              │    │
│  │  │ (StatefulSet)│  │ (StatefulSet)│              │    │
│  │  │  + PVC       │  │  + PVC       │              │    │
│  │  └──────────────┘  └──────────────┘              │    │
│  │                                                     │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │         Monitoring Namespace                        │    │
│  │                                                     │    │
│  │  ┌──────────────┐      ┌──────────────┐           │    │
│  │  │  Prometheus  │──────│   Grafana    │           │    │
│  │  └──────────────┘      └──────────────┘           │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. Flask Web Application

**Purpose**: Control plane and user interface

**Responsibilities**:
- Serve web dashboard (Jinja2 templates + Alpine.js/HTMX)
- Handle user authentication and authorization
- Expose REST API for server management
- Interact with Kubernetes API to manage game servers
- Stream logs from game server pods
- Provide WebSocket connections for real-time console

**Technologies**:
- Flask (web framework)
- Flask-SQLAlchemy (ORM)
- Flask-Login (authentication)
- Kubernetes Python client
- Flask-SocketIO (WebSocket for console)
- Alpine.js/HTMX (frontend interactivity)

**Deployment**:
- Kubernetes Deployment
- ClusterIP Service
- Horizontal Pod Autoscaling (optional)

### 2. PostgreSQL Database

**Purpose**: Persistent data storage

**Schema**:
- Users (accounts, passwords, roles)
- Servers (configuration, status, metadata)
- Permissions (user-server relationships, fine-grained permissions)
- Templates (server templates/eggs)
- Resource Plans (CPU/RAM presets)
- Audit Logs (user actions)

**Deployment**:
- StatefulSet with PersistentVolumeClaim
- ClusterIP Service
- Regular backups via CronJob

### 3. Game Server Pods

**Purpose**: Run Minecraft servers

**Architecture**:
- Each server runs as a StatefulSet (single replica)
- PersistentVolumeClaim for world data, configs, plugins
- Resource limits/requests based on plan
- Init containers for downloading server JAR files

**Deployment**:
- StatefulSet per server
- ClusterIP Service (for now, future: LoadBalancer/NodePort)
- PVC for persistent storage

### 4. Monitoring Stack

**Purpose**: Metrics and observability

**Components**:
- Prometheus: Scrape metrics from Flask app and game servers
- Grafana: Dashboards for panel metrics (not game server metrics)

**Metrics**:
- Panel health (request rate, errors, latency)
- Database connection pool
- Active users
- Server creation/deletion rate
- Resource utilization (panel only)

## Data Flow

### Server Creation Flow

1. User submits server creation form via web UI
2. Flask validates request and checks user permissions/quotas
3. Flask creates database record for new server
4. Flask calls Kubernetes API to create:
   - PersistentVolumeClaim for server data
   - StatefulSet with Minecraft container
   - Service for server networking
5. Flask watches pod status and updates database
6. User sees server appear in dashboard with "Starting" status

### Console Interaction Flow

1. User opens server console in web UI
2. Browser establishes WebSocket connection to Flask
3. Flask authenticates user and verifies server permissions
4. Flask streams pod logs via Kubernetes API to WebSocket
5. User sends command via WebSocket
6. Flask executes command in pod via `kubectl exec`
7. Output streamed back through WebSocket to browser

### File Manager Flow

1. User browses to file manager for a server
2. Flask lists files by executing `ls` in pod
3. User clicks file to edit
4. Flask reads file content via `kubectl exec cat`
5. User edits and saves
6. Flask writes file via `kubectl exec tee`

## Security Architecture

### Authentication
- Password hashing with bcrypt
- Session-based authentication with secure cookies
- CSRF protection on all forms

### Authorization
- Fine-grained permissions stored in database
- Permission checks on every API call
- Three levels:
  1. Global (admin access)
  2. Server-level (owner, sub-user)
  3. Action-level (console, files, control)

### Kubernetes RBAC
- ServiceAccount for Flask app
- ClusterRole with permissions:
  - Create/delete/update StatefulSets, PVCs, Services
  - Get/list/watch pods
  - Exec into pods
  - Read logs
- Limited to specific namespaces

### Network Security
- NetworkPolicies to isolate game servers
- Panel only accessible via ClusterIP (internal)
- Future: Ingress with TLS

## Scalability Considerations

### Panel Scaling
- Stateless Flask app (sessions in DB)
- Horizontal pod autoscaling based on CPU/requests
- PostgreSQL connection pooling

### Game Server Scaling
- Each server isolated in own pod
- Resource quotas prevent resource exhaustion
- Support for hundreds of small servers or dozens of large servers

### Storage Scaling
- PVCs can be expanded without downtime
- Future: StorageClass with dynamic provisioning
- Backup to object storage for archival

## Deployment Strategy

### Development
- Local testing with kind/k3s
- SQLite for local development
- Port-forward to access panel

### Production
- Self-hosted on-prem Kubernetes cluster
- PostgreSQL with replication
- Helm chart deployment via ArgoCD
- GitHub Actions builds images, pushes to ghcr.io
- Prometheus/Grafana for monitoring
