# AI Implementation Checklist

This is a comprehensive, step-by-step checklist for an AI assistant to implement the Kubernetes Game Server Panel. Each task includes specific files to create, code to write, and verification steps.

## Phase 0: Project Setup

### Task 0.1: Create Project Structure
- [ ] Create root directory structure:
  ```
  server-panel/
  ├── app/                    # Flask application
  ├── helm/                   # Helm chart
  ├── .github/workflows/      # GitHub Actions
  ├── tests/                  # Test files
  ├── docs/                   # Documentation
  └── ai_docs/                # AI-specific docs
  ```
- [ ] Create `.gitignore` file
- [ ] Create `README.md` with project description
- [ ] Verify: All directories exist using `ls` command

### Task 0.2: Initialize Git Repository
- [ ] Run `git init`
- [ ] Create initial commit
- [ ] Verify: `git status` shows clean working tree

### Task 0.3: Create Python Virtual Environment
- [ ] Run `python -m venv venv`
- [ ] Activate venv: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
- [ ] Verify: `which python` shows venv path

### Task 0.4: Create Requirements File
- [ ] Create `requirements.txt` with dependencies:
  ```
  Flask==3.0.0
  Flask-SQLAlchemy==3.1.1
  Flask-Login==0.6.3
  Flask-SocketIO==5.3.5
  psycopg2-binary==2.9.9
  kubernetes==28.1.0
  bcrypt==4.1.1
  python-dotenv==1.0.0
  gunicorn==21.2.0
  prometheus-flask-exporter==0.23.0
  ```
- [ ] Create `requirements-dev.txt`:
  ```
  pytest==7.4.3
  pytest-cov==4.1.0
  black==23.12.0
  flake8==6.1.0
  mypy==1.7.1
  ```
- [ ] Install: `pip install -r requirements.txt -r requirements-dev.txt`
- [ ] Verify: `pip list` shows all packages

## Phase 1: Flask Application Structure

### Task 1.1: Create Flask Application Directory Structure
- [ ] Create the following structure inside `app/`:
  ```
  app/
  ├── __init__.py              # Flask app factory
  ├── config.py                # Configuration
  ├── models.py                # Database models
  ├── auth/                    # Authentication blueprint
  │   ├── __init__.py
  │   ├── routes.py
  │   └── forms.py
  ├── servers/                 # Server management blueprint
  │   ├── __init__.py
  │   ├── routes.py
  │   └── kubernetes_client.py
  ├── console/                 # Console blueprint
  │   ├── __init__.py
  │   └── routes.py
  ├── files/                   # File manager blueprint
  │   ├── __init__.py
  │   └── routes.py
  ├── api/                     # REST API blueprint
  │   ├── __init__.py
  │   └── routes.py
  ├── templates/               # Jinja2 templates
  │   ├── base.html
  │   ├── auth/
  │   ├── servers/
  │   ├── console/
  │   └── files/
  └── static/                  # Static files
      ├── css/
      ├── js/
      └── images/
  ```
- [ ] Create all `__init__.py` files (can be empty for now)
- [ ] Verify: Tree structure matches above

### Task 1.2: Create Configuration File
- [ ] Create `app/config.py`:
  ```python
  import os
  from datetime import timedelta

  class Config:
      # Flask
      SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

      # Database
      SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:postgres@localhost:5432/serverpanel'
      SQLALCHEMY_TRACK_MODIFICATIONS = False

      # Session
      PERMANENT_SESSION_LIFETIME = timedelta(days=7)

      # Kubernetes
      K8S_NAMESPACE = os.environ.get('K8S_NAMESPACE') or 'game-servers'
      K8S_IN_CLUSTER = os.environ.get('K8S_IN_CLUSTER', 'false').lower() == 'true'

  class DevelopmentConfig(Config):
      DEBUG = True

  class ProductionConfig(Config):
      DEBUG = False

  config = {
      'development': DevelopmentConfig,
      'production': ProductionConfig,
      'default': DevelopmentConfig
  }
  ```
- [ ] Verify: File syntax is correct with `python -m py_compile app/config.py`

### Task 1.3: Create Database Models
- [ ] Create `app/models.py`:
  ```python
  from datetime import datetime
  from flask_sqlalchemy import SQLAlchemy
  from flask_login import UserMixin
  from werkzeug.security import generate_password_hash, check_password_hash

  db = SQLAlchemy()

  class User(UserMixin, db.Model):
      __tablename__ = 'users'

      id = db.Column(db.Integer, primary_key=True)
      email = db.Column(db.String(255), unique=True, nullable=False, index=True)
      password_hash = db.Column(db.String(255), nullable=False)
      is_admin = db.Column(db.Boolean, default=False)
      created_at = db.Column(db.DateTime, default=datetime.utcnow)

      # Resource quotas
      max_cpu_cores = db.Column(db.Integer, default=8)
      max_ram_gb = db.Column(db.Integer, default=16)
      max_servers = db.Column(db.Integer, default=5)

      # Relationships
      servers = db.relationship('Server', backref='owner', lazy='dynamic', cascade='all, delete-orphan')

      def set_password(self, password):
          self.password_hash = generate_password_hash(password)

      def check_password(self, password):
          return check_password_hash(self.password_hash, password)

  class Server(db.Model):
      __tablename__ = 'servers'

      id = db.Column(db.Integer, primary_key=True)
      name = db.Column(db.String(100), nullable=False)
      owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

      # Server configuration
      server_type = db.Column(db.String(50), nullable=False)  # vanilla, paper, forge, etc.
      server_version = db.Column(db.String(20), nullable=False)  # 1.20.1

      # Resources
      cpu_cores = db.Column(db.Integer, nullable=False)
      ram_mb = db.Column(db.Integer, nullable=False)
      disk_gb = db.Column(db.Integer, nullable=False)

      # Kubernetes identifiers
      pod_name = db.Column(db.String(255))
      pvc_name = db.Column(db.String(255))
      service_name = db.Column(db.String(255))

      # Status
      status = db.Column(db.String(20), default='creating')  # creating, starting, running, stopping, stopped, error

      created_at = db.Column(db.DateTime, default=datetime.utcnow)
      updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

      # Relationships
      permissions = db.relationship('ServerPermission', backref='server', lazy='dynamic', cascade='all, delete-orphan')

      def __repr__(self):
          return f'<Server {self.name}>'

  class ServerPermission(db.Model):
      __tablename__ = 'server_permissions'

      id = db.Column(db.Integer, primary_key=True)
      server_id = db.Column(db.Integer, db.ForeignKey('servers.id'), nullable=False)
      user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

      # Permissions
      can_view = db.Column(db.Boolean, default=True)
      can_console = db.Column(db.Boolean, default=False)
      can_files = db.Column(db.Boolean, default=False)
      can_control = db.Column(db.Boolean, default=False)  # start/stop/restart
      can_config = db.Column(db.Boolean, default=False)
      can_delete = db.Column(db.Boolean, default=False)

      created_at = db.Column(db.DateTime, default=datetime.utcnow)

      user = db.relationship('User', backref='server_permissions')

  class ServerTemplate(db.Model):
      __tablename__ = 'server_templates'

      id = db.Column(db.Integer, primary_key=True)
      name = db.Column(db.String(100), nullable=False, unique=True)
      description = db.Column(db.Text)
      server_type = db.Column(db.String(50), nullable=False)
      server_version = db.Column(db.String(20), nullable=False)

      # Default resources
      default_cpu = db.Column(db.Integer, default=2)
      default_ram_mb = db.Column(db.Integer, default=4096)
      default_disk_gb = db.Column(db.Integer, default=20)

      # Startup configuration
      startup_command = db.Column(db.Text)
      environment_vars = db.Column(db.JSON)  # JSON object

      created_at = db.Column(db.DateTime, default=datetime.utcnow)

  class AuditLog(db.Model):
      __tablename__ = 'audit_logs'

      id = db.Column(db.Integer, primary_key=True)
      user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
      action = db.Column(db.String(100), nullable=False)
      resource_type = db.Column(db.String(50))  # server, user, etc.
      resource_id = db.Column(db.Integer)
      details = db.Column(db.JSON)
      ip_address = db.Column(db.String(45))
      created_at = db.Column(db.DateTime, default=datetime.utcnow)

      user = db.relationship('User', backref='audit_logs')
  ```
- [ ] Verify: File syntax with `python -m py_compile app/models.py`

### Task 1.4: Create Flask App Factory
- [ ] Create `app/__init__.py`:
  ```python
  from flask import Flask
  from flask_login import LoginManager
  from app.config import config
  from app.models import db, User

  login_manager = LoginManager()

  @login_manager.user_loader
  def load_user(user_id):
      return User.query.get(int(user_id))

  def create_app(config_name='default'):
      app = Flask(__name__)
      app.config.from_object(config[config_name])

      # Initialize extensions
      db.init_app(app)
      login_manager.init_app(app)
      login_manager.login_view = 'auth.login'

      # Register blueprints
      from app.auth import auth as auth_blueprint
      app.register_blueprint(auth_blueprint, url_prefix='/auth')

      from app.servers import servers as servers_blueprint
      app.register_blueprint(servers_blueprint, url_prefix='/servers')

      from app.console import console as console_blueprint
      app.register_blueprint(console_blueprint, url_prefix='/console')

      from app.files import files as files_blueprint
      app.register_blueprint(files_blueprint, url_prefix='/files')

      from app.api import api as api_blueprint
      app.register_blueprint(api_blueprint, url_prefix='/api')

      # Create tables
      with app.app_context():
          db.create_all()

      return app
  ```
- [ ] Verify: Import check with `python -c "from app import create_app"`

### Task 1.5: Create Run Script
- [ ] Create `run.py` in root directory:
  ```python
  from app import create_app
  import os

  app = create_app(os.getenv('FLASK_ENV') or 'development')

  if __name__ == '__main__':
      app.run(host='0.0.0.0', port=5000)
  ```
- [ ] Verify: Can run with `python run.py` (will fail to connect to DB, that's expected)

## Phase 2: Authentication System

### Task 2.1: Create Authentication Blueprint
- [ ] Create `app/auth/__init__.py`:
  ```python
  from flask import Blueprint

  auth = Blueprint('auth', __name__)

  from app.auth import routes
  ```

### Task 2.2: Create Auth Routes
- [ ] Create `app/auth/routes.py`:
  ```python
  from flask import render_template, redirect, url_for, flash, request
  from flask_login import login_user, logout_user, login_required
  from app.auth import auth
  from app.models import db, User

  @auth.route('/login', methods=['GET', 'POST'])
  def login():
      if request.method == 'POST':
          email = request.form.get('email')
          password = request.form.get('password')
          remember = request.form.get('remember', False)

          user = User.query.filter_by(email=email).first()

          if user and user.check_password(password):
              login_user(user, remember=remember)
              next_page = request.args.get('next')
              return redirect(next_page or url_for('servers.dashboard'))
          else:
              flash('Invalid email or password', 'error')

      return render_template('auth/login.html')

  @auth.route('/register', methods=['GET', 'POST'])
  def register():
      if request.method == 'POST':
          email = request.form.get('email')
          password = request.form.get('password')

          if User.query.filter_by(email=email).first():
              flash('Email already registered', 'error')
              return redirect(url_for('auth.register'))

          user = User(email=email)
          user.set_password(password)
          db.session.add(user)
          db.session.commit()

          flash('Registration successful! Please log in.', 'success')
          return redirect(url_for('auth.login'))

      return render_template('auth/register.html')

  @auth.route('/logout')
  @login_required
  def logout():
      logout_user()
      return redirect(url_for('auth.login'))
  ```
- [ ] Verify: Syntax check

### Task 2.3: Create Auth Templates
- [ ] Create `app/templates/base.html`:
  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>{% block title %}Server Panel{% endblock %}</title>
      <script src="https://cdn.tailwindcss.com"></script>
      <script src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js" defer></script>
      <script src="https://unpkg.com/htmx.org@1.9.10"></script>
  </head>
  <body class="bg-gray-100">
      <nav class="bg-blue-600 text-white p-4">
          <div class="container mx-auto flex justify-between items-center">
              <h1 class="text-2xl font-bold">Server Panel</h1>
              {% if current_user.is_authenticated %}
              <div class="space-x-4">
                  <a href="{{ url_for('servers.dashboard') }}" class="hover:underline">Dashboard</a>
                  <a href="{{ url_for('auth.logout') }}" class="hover:underline">Logout</a>
              </div>
              {% endif %}
          </div>
      </nav>

      <div class="container mx-auto mt-8 px-4">
          {% with messages = get_flashed_messages(with_categories=true) %}
              {% if messages %}
                  {% for category, message in messages %}
                  <div class="p-4 mb-4 rounded {% if category == 'error' %}bg-red-100 text-red-700{% else %}bg-green-100 text-green-700{% endif %}">
                      {{ message }}
                  </div>
                  {% endfor %}
              {% endif %}
          {% endwith %}

          {% block content %}{% endblock %}
      </div>
  </body>
  </html>
  ```
- [ ] Create `app/templates/auth/login.html`
- [ ] Create `app/templates/auth/register.html`
- [ ] Verify: Templates exist

## Phase 3: Kubernetes Integration

### Task 3.1: Create Kubernetes Client Module
- [ ] Create `app/servers/kubernetes_client.py`:
  ```python
  from kubernetes import client, config
  from kubernetes.client.rest import ApiException
  import os

  class KubernetesClient:
      def __init__(self):
          if os.getenv('K8S_IN_CLUSTER', 'false').lower() == 'true':
              config.load_incluster_config()
          else:
              config.load_kube_config()

          self.core_api = client.CoreV1Api()
          self.apps_api = client.AppsV1Api()
          self.namespace = os.getenv('K8S_NAMESPACE', 'game-servers')

      def create_minecraft_server(self, server_name, server_config):
          # Create PVC
          pvc = self._create_pvc(server_name, server_config['disk_gb'])

          # Create StatefulSet
          statefulset = self._create_statefulset(server_name, server_config)

          # Create Service
          service = self._create_service(server_name)

          return {
              'pvc_name': pvc.metadata.name,
              'pod_name': f"{server_name}-0",
              'service_name': service.metadata.name
          }

      def _create_pvc(self, name, size_gb):
          pvc = client.V1PersistentVolumeClaim(
              metadata=client.V1ObjectMeta(name=f"{name}-data"),
              spec=client.V1PersistentVolumeClaimSpec(
                  access_modes=['ReadWriteOnce'],
                  resources=client.V1ResourceRequirements(
                      requests={'storage': f'{size_gb}Gi'}
                  )
              )
          )
          return self.core_api.create_namespaced_persistent_volume_claim(
              namespace=self.namespace,
              body=pvc
          )

      def _create_statefulset(self, name, config):
          # TODO: Implement StatefulSet creation
          pass

      def _create_service(self, name):
          # TODO: Implement Service creation
          pass

      def delete_server(self, server_name):
          # Delete StatefulSet
          # Delete PVC
          # Delete Service
          pass

      def get_server_status(self, pod_name):
          try:
              pod = self.core_api.read_namespaced_pod(
                  name=pod_name,
                  namespace=self.namespace
              )
              return pod.status.phase
          except ApiException:
              return 'Unknown'

      def start_server(self, server_name):
          # Scale StatefulSet to 1
          pass

      def stop_server(self, server_name):
          # Scale StatefulSet to 0
          pass

      def get_server_logs(self, pod_name, tail_lines=100):
          try:
              logs = self.core_api.read_namespaced_pod_log(
                  name=pod_name,
                  namespace=self.namespace,
                  tail_lines=tail_lines
              )
              return logs
          except ApiException as e:
              return f"Error fetching logs: {str(e)}"

      def exec_command(self, pod_name, command):
          # Execute command in pod
          pass
  ```
- [ ] Verify: Import test

### Task 3.2: Create Server Management Routes
- [ ] Implement server CRUD in `app/servers/routes.py`
- [ ] Create dashboard view
- [ ] Create server creation form
- [ ] Add server control endpoints (start/stop/restart)
- [ ] Verify: Routes registered

## Phase 4: Console Implementation

### Task 4.1: Set Up WebSocket
- [ ] Install flask-socketio
- [ ] Create WebSocket event handlers in `app/console/routes.py`
- [ ] Implement log streaming from Kubernetes pods
- [ ] Implement command execution
- [ ] Verify: WebSocket connection works

### Task 4.2: Create Console UI
- [ ] Create terminal-like UI with `app/templates/console/console.html`
- [ ] Add JavaScript for WebSocket connection
- [ ] Add command input form
- [ ] Add auto-scroll functionality
- [ ] Verify: Can view logs and send commands

## Phase 5: File Manager

### Task 5.1: Create File Browser Backend
- [ ] Implement file listing via kubectl exec in `app/files/routes.py`
- [ ] Implement file read/write endpoints
- [ ] Implement file delete endpoint
- [ ] Verify: Can list files via API

### Task 5.2: Create File Manager UI
- [ ] Create file browser template
- [ ] Add file upload functionality
- [ ] Add file editor with syntax highlighting
- [ ] Verify: Can browse and edit files

## Phase 6: Docker & Helm

### Task 6.1: Create Dockerfile
- [ ] Create multi-stage Dockerfile
- [ ] Add health check
- [ ] Test local build: `docker build -t server-panel .`
- [ ] Verify: Container runs locally

### Task 6.2: Create Helm Chart
- [ ] Generate Helm chart: `helm create helm/server-panel`
- [ ] Update Chart.yaml with project info
- [ ] Create values.yaml with configuration options
- [ ] Create templates for:
  - Deployment
  - Service
  - ServiceAccount
  - Role
  - RoleBinding
  - ConfigMap
  - Secret
- [ ] Verify: `helm lint helm/server-panel`

## Phase 7: CI/CD

### Task 7.1: Create GitHub Actions Workflow
- [ ] Create `.github/workflows/ci.yml` for linting and tests
- [ ] Create `.github/workflows/build.yml` for Docker build
- [ ] Add workflow to push to ghcr.io
- [ ] Verify: Workflows pass on push

### Task 7.2: Set Up ArgoCD Application
- [ ] Create ArgoCD Application manifest
- [ ] Configure sync policy
- [ ] Verify: ArgoCD deploys successfully

## Phase 8: Monitoring

### Task 8.1: Add Prometheus Metrics
- [ ] Install prometheus-flask-exporter
- [ ] Add custom metrics for server operations
- [ ] Create /metrics endpoint
- [ ] Verify: Metrics accessible

### Task 8.2: Create Grafana Dashboard
- [ ] Create dashboard JSON
- [ ] Import into Grafana
- [ ] Verify: Dashboard displays metrics

## Phase 9: Testing

### Task 9.1: Write Unit Tests
- [ ] Test authentication functions
- [ ] Test database models
- [ ] Test Kubernetes client methods
- [ ] Run: `pytest tests/unit/`
- [ ] Verify: All tests pass

### Task 9.2: Write Integration Tests
- [ ] Test server creation flow
- [ ] Test console functionality
- [ ] Test file operations
- [ ] Run: `pytest tests/integration/`
- [ ] Verify: All tests pass

## Phase 10: Documentation

### Task 10.1: Update README
- [ ] Add setup instructions
- [ ] Add deployment guide
- [ ] Add API documentation
- [ ] Verify: Instructions work for fresh install

### Task 10.2: Create User Guide
- [ ] Document how to create servers
- [ ] Document console usage
- [ ] Document file management
- [ ] Verify: Clear for end users

## Verification Checklist

After completing all tasks, verify:
- [ ] Flask app runs without errors
- [ ] Can register and log in
- [ ] Can create a Minecraft server
- [ ] Server appears in Kubernetes: `kubectl get pods -n game-servers`
- [ ] Can access server console
- [ ] Can view and edit server files
- [ ] Docker image builds successfully
- [ ] Helm chart installs without errors
- [ ] GitHub Actions workflows pass
- [ ] Prometheus metrics are collected
- [ ] All tests pass
- [ ] Documentation is complete
