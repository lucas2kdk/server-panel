# Glossary - Technical Terms Explained

This document explains all technical terms used in the project for developers new to Kubernetes, Flask, or game server hosting.

## Kubernetes Terms

### Pod
A pod is the smallest deployable unit in Kubernetes. Think of it as a wrapper around one or more containers. In our case, each Minecraft server runs in its own pod.

**Example**: When you create a Minecraft server, a pod is created that contains the Minecraft server software.

### StatefulSet
A Kubernetes resource that manages pods that need persistent storage and stable identities. Unlike regular Deployments, StatefulSets ensure that if a pod restarts, it gets the same storage and name.

**Why we use it**: Minecraft servers need their world data to persist even if the pod crashes. StatefulSets ensure the server pod always reconnects to the same storage.

### PersistentVolumeClaim (PVC)
A request for storage in Kubernetes. It's like asking for a hard drive that will persist even if your pod is deleted.

**Example**: Each Minecraft server gets a PVC to store its world files, plugins, and configuration.

### Service
A stable network endpoint to access pods. Even if pods restart and get new IP addresses, the Service IP stays the same.

**Types**:
- **ClusterIP**: Only accessible inside the Kubernetes cluster
- **NodePort**: Accessible on a specific port on each cluster node
- **LoadBalancer**: Creates an external load balancer (cloud only)

### Namespace
A way to organize and isolate resources in Kubernetes. Think of it like folders on your computer.

**Our namespaces**:
- `panel`: Where the Flask app and database run
- `game-servers`: Where all Minecraft servers run
- `monitoring`: Where Prometheus and Grafana run

### Deployment
A Kubernetes resource that manages stateless applications. It handles rolling updates, scaling, and ensures the desired number of pods are running.

**Example**: The Flask application runs as a Deployment because it doesn't need persistent storage.

### RBAC (Role-Based Access Control)
Kubernetes' permission system. It controls what operations a ServiceAccount can perform.

**Example**: Our Flask app needs permission to create Minecraft server pods, so we give its ServiceAccount a Role with those permissions.

### ServiceAccount
An identity for processes running in pods. It's like a user account, but for applications instead of humans.

**Example**: The Flask app uses a ServiceAccount to authenticate with the Kubernetes API.

### Helm
A package manager for Kubernetes. Think of it like npm for Node.js or pip for Python, but for Kubernetes applications.

**Helm Chart**: A bundle of Kubernetes configuration files that can be installed as a unit.

### ArgoCD
A GitOps tool that automatically deploys applications to Kubernetes when code changes in Git.

**How it works**: When we push a new Helm chart version to Git, ArgoCD detects the change and updates our Kubernetes deployment.

## Flask Terms

### Flask
A lightweight Python web framework for building web applications and APIs.

**Example**: We use Flask to build the web dashboard and API endpoints.

### Jinja2
A templating engine for Python. It lets you write HTML with embedded Python code.

**Example**:
```html
<h1>Welcome, {{ username }}!</h1>
```

### Blueprint
A way to organize Flask routes into modules. Like splitting your app into sections.

**Example**: We might have a `servers` blueprint for server management and an `auth` blueprint for login/logout.

### Route
A URL path in your Flask app that triggers a function.

**Example**:
```python
@app.route('/servers')
def list_servers():
    return render_template('servers.html')
```

### SQLAlchemy
An ORM (Object-Relational Mapping) library that lets you work with databases using Python objects instead of SQL queries.

**Example**:
```python
# Instead of: SELECT * FROM users WHERE id = 1
user = User.query.get(1)
```

### Flask-Login
A Flask extension that handles user authentication (login/logout/sessions).

### WebSocket
A protocol for two-way communication between browser and server. Unlike HTTP (request-response), WebSocket keeps a connection open for real-time data.

**Example**: We use WebSocket to stream Minecraft server logs to the browser in real-time.

## Frontend Terms

### Alpine.js
A minimal JavaScript framework for adding interactivity to HTML. Lighter alternative to React/Vue.

**Example**:
```html
<div x-data="{ open: false }">
  <button @click="open = !open">Toggle</button>
  <div x-show="open">Content</div>
</div>
```

### HTMX
A library that lets you access modern browser features (AJAX, WebSockets) directly in HTML without writing JavaScript.

**Example**:
```html
<button hx-post="/servers/start/1" hx-swap="outerHTML">
  Start Server
</button>
```

## Database Terms

### PostgreSQL
A powerful, open-source relational database. More feature-rich than MySQL.

### ORM (Object-Relational Mapping)
A technique that lets you interact with databases using objects in your programming language instead of writing SQL.

**Example**:
```python
# ORM way
server = Server(name="My Server", ram=4096)
db.session.add(server)
db.session.commit()

# SQL way
db.execute("INSERT INTO servers (name, ram) VALUES ('My Server', 4096)")
```

### Migration
A version-controlled database schema change. Migrations let you track and apply database changes over time.

**Example**: Adding a new column to the `servers` table is a migration.

## CI/CD Terms

### CI/CD (Continuous Integration / Continuous Deployment)
Automated pipeline that builds, tests, and deploys code changes.

**Our pipeline**:
1. Developer pushes code to GitHub
2. GitHub Actions runs tests
3. GitHub Actions builds Docker image
4. GitHub Actions pushes image to GitHub Container Registry
5. ArgoCD detects new image and deploys to Kubernetes

### GitHub Actions
GitHub's built-in CI/CD system. You define workflows in YAML files.

**Example**: When you push code, GitHub Actions can automatically run tests and build Docker images.

### Docker Image
A packaged application with all its dependencies. Think of it like a .exe file that includes the entire operating system.

**Example**: We package the Flask app and all Python libraries into a Docker image.

### Container Registry
A storage location for Docker images. Like Docker Hub, but we use GitHub Container Registry (ghcr.io).

## Monitoring Terms

### Prometheus
A monitoring system that collects metrics (numbers over time) from applications.

**Example**: Number of HTTP requests per second, memory usage, etc.

### Grafana
A visualization tool that creates dashboards from Prometheus data.

**Example**: Charts showing server creation rate, API latency, etc.

### Metrics
Numerical measurements over time. Used to track application health and performance.

**Examples**:
- `http_requests_total`: Total number of HTTP requests
- `memory_usage_bytes`: Current memory consumption

## Minecraft Server Terms

### Vanilla
The official, unmodified Minecraft server from Mojang.

### Paper/Spigot/Bukkit
Modified Minecraft servers that support plugins (mods that add features without modifying game code).

**Spigot**: Performance-optimized Minecraft server
**Paper**: Fork of Spigot with more optimizations
**Bukkit**: API for writing plugins

### Forge/Fabric
Mod loaders that allow extensive game modifications.

**Forge**: Older, widely-used mod loader
**Fabric**: Newer, lightweight mod loader

### Server JAR
The Java executable file that runs the Minecraft server.

**Example**: `paper-1.20.1-196.jar`

### Eggs (Pterodactyl term)
Pre-configured server templates. Instead of manually configuring a server, you select an "egg" that has everything pre-set.

**Example**: A "Paper 1.20" egg knows to download the correct JAR, set JVM flags, and configure ports.

## Network Terms

### Port
A numbered endpoint for network connections. Like apartment numbers in a building.

**Example**: Minecraft default port is 25565

### Ingress
Kubernetes resource that routes external HTTP/HTTPS traffic to services inside the cluster.

**Example**: An Ingress could route `panel.example.com` to the Flask app service.

### LoadBalancer
A service that distributes traffic across multiple pods and provides an external IP address.

## Resource Management Terms

### CPU Limit
Maximum CPU a pod can use. Measured in cores or millicores (1000m = 1 core).

**Example**: A small Minecraft server might have a limit of `1000m` (1 CPU core).

### Memory Limit
Maximum RAM a pod can use. Measured in bytes (Mi = Mebibytes, Gi = Gibibytes).

**Example**: A medium Minecraft server might have `4Gi` (4 gigabytes) of RAM.

### Resource Quota
A limit on total resources a user or namespace can consume.

**Example**: A user might be limited to 8 CPU cores and 16Gi RAM total across all their servers.
