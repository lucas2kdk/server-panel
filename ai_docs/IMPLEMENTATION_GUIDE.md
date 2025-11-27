# Implementation Guide for AI

This guide provides specific code patterns, examples, and implementation details for building each component of the system.

## 1. Database Models - Detailed Implementation

### User Model with Resource Tracking

```python
from app.models import db, User, Server

class User(UserMixin, db.Model):
    # ... (fields from checklist)

    def get_resource_usage(self):
        """Calculate current resource usage across all servers."""
        total_cpu = sum(server.cpu_cores for server in self.servers.filter_by(status='running'))
        total_ram = sum(server.ram_mb for server in self.servers.filter_by(status='running'))
        server_count = self.servers.count()

        return {
            'cpu_used': total_cpu,
            'cpu_max': self.max_cpu_cores,
            'cpu_percent': (total_cpu / self.max_cpu_cores * 100) if self.max_cpu_cores > 0 else 0,
            'ram_used_mb': total_ram,
            'ram_max_mb': self.max_ram_gb * 1024,
            'ram_percent': (total_ram / (self.max_ram_gb * 1024) * 100) if self.max_ram_gb > 0 else 0,
            'servers_used': server_count,
            'servers_max': self.max_servers,
        }

    def can_create_server(self, cpu_cores, ram_mb):
        """Check if user has quota for new server."""
        usage = self.get_resource_usage()

        if usage['servers_used'] >= self.max_servers:
            return False, "Server limit reached"

        if usage['cpu_used'] + cpu_cores > self.max_cpu_cores:
            return False, "CPU quota exceeded"

        if usage['ram_used_mb'] + ram_mb > (self.max_ram_gb * 1024):
            return False, "RAM quota exceeded"

        return True, None
```

### Server Model with Kubernetes Name Generation

```python
class Server(db.Model):
    # ... (fields from checklist)

    @staticmethod
    def generate_k8s_name(owner_id, server_name):
        """Generate Kubernetes-compliant resource name."""
        import re
        # K8s names must be lowercase alphanumeric + hyphens, max 63 chars
        safe_name = re.sub(r'[^a-z0-9-]', '', server_name.lower().replace(' ', '-'))
        return f"mc-{owner_id}-{safe_name}"[:63]

    def to_dict(self):
        """Serialize server for API responses."""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.server_type,
            'version': self.server_version,
            'status': self.status,
            'resources': {
                'cpu': self.cpu_cores,
                'ram_mb': self.ram_mb,
                'disk_gb': self.disk_gb
            },
            'created_at': self.created_at.isoformat(),
            'pod_name': self.pod_name
        }
```

## 2. Kubernetes Client - Complete Implementation

### StatefulSet Creation

```python
def _create_statefulset(self, name, config):
    """Create StatefulSet for Minecraft server."""
    # Container definition
    container = client.V1Container(
        name="minecraft",
        image=self._get_server_image(config['server_type']),
        ports=[client.V1ContainerPort(container_port=25565, name="minecraft")],
        env=[
            client.V1EnvVar(name="EULA", value="TRUE"),
            client.V1EnvVar(name="TYPE", value=config['server_type'].upper()),
            client.V1EnvVar(name="VERSION", value=config['server_version']),
            client.V1EnvVar(name="MEMORY", value=f"{config['ram_mb']}M"),
        ],
        resources=client.V1ResourceRequirements(
            requests={
                'cpu': f"{config['cpu_cores']}",
                'memory': f"{config['ram_mb']}Mi"
            },
            limits={
                'cpu': f"{config['cpu_cores']}",
                'memory': f"{config['ram_mb']}Mi"
            }
        ),
        volume_mounts=[
            client.V1VolumeMount(
                name="data",
                mount_path="/data"
            )
        ]
    )

    # Pod template
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(
            labels={
                "app": "minecraft",
                "server": name
            }
        ),
        spec=client.V1PodSpec(
            containers=[container],
            volumes=[]  # VolumeClaimTemplates will provide storage
        )
    )

    # VolumeClaimTemplate
    volume_claim_template = client.V1PersistentVolumeClaim(
        metadata=client.V1ObjectMeta(name="data"),
        spec=client.V1PersistentVolumeClaimSpec(
            access_modes=["ReadWriteOnce"],
            resources=client.V1ResourceRequirements(
                requests={'storage': f"{config['disk_gb']}Gi"}
            )
        )
    )

    # StatefulSet
    statefulset = client.V1StatefulSet(
        metadata=client.V1ObjectMeta(name=name),
        spec=client.V1StatefulSetSpec(
            service_name=name,
            replicas=1,
            selector=client.V1LabelSelector(
                match_labels={"app": "minecraft", "server": name}
            ),
            template=template,
            volume_claim_templates=[volume_claim_template]
        )
    )

    return self.apps_api.create_namespaced_stateful_set(
        namespace=self.namespace,
        body=statefulset
    )

def _get_server_image(self, server_type):
    """Get Docker image for server type."""
    images = {
        'vanilla': 'itzg/minecraft-server:latest',
        'paper': 'itzg/minecraft-server:latest',
        'spigot': 'itzg/minecraft-server:latest',
        'forge': 'itzg/minecraft-server:latest',
        'fabric': 'itzg/minecraft-server:latest'
    }
    return images.get(server_type, 'itzg/minecraft-server:latest')
```

### Log Streaming with Watch

```python
from kubernetes import watch

def stream_logs(self, pod_name, callback):
    """Stream logs from pod to callback function."""
    w = watch.Watch()
    try:
        for line in w.stream(
            self.core_api.read_namespaced_pod_log,
            name=pod_name,
            namespace=self.namespace,
            follow=True
        ):
            callback(line)
    except ApiException as e:
        callback(f"Error streaming logs: {str(e)}")
```

### Command Execution

```python
from kubernetes.stream import stream

def exec_command(self, pod_name, command):
    """Execute command in pod and return output."""
    try:
        resp = stream(
            self.core_api.connect_get_namespaced_pod_exec,
            pod_name,
            self.namespace,
            command=command,
            stderr=True,
            stdin=False,
            stdout=True,
            tty=False
        )
        return resp
    except ApiException as e:
        return f"Error: {str(e)}"
```

## 3. Server Management Routes

### Server Creation with Validation

```python
from flask import request, jsonify, render_template
from flask_login import login_required, current_user
from app.servers import servers
from app.models import db, Server
from app.servers.kubernetes_client import KubernetesClient

k8s = KubernetesClient()

@servers.route('/create', methods=['GET', 'POST'])
@login_required
def create_server():
    if request.method == 'POST':
        name = request.form.get('name')
        server_type = request.form.get('type')
        version = request.form.get('version')
        plan = request.form.get('plan')  # small, medium, large

        # Resource mapping
        plans = {
            'small': {'cpu': 1, 'ram': 2048, 'disk': 10},
            'medium': {'cpu': 2, 'ram': 4096, 'disk': 20},
            'large': {'cpu': 4, 'ram': 8192, 'disk': 40}
        }

        resources = plans.get(plan)
        if not resources:
            flash('Invalid resource plan', 'error')
            return redirect(url_for('servers.create_server'))

        # Check quota
        can_create, error = current_user.can_create_server(
            resources['cpu'],
            resources['ram']
        )
        if not can_create:
            flash(error, 'error')
            return redirect(url_for('servers.create_server'))

        # Create database record
        k8s_name = Server.generate_k8s_name(current_user.id, name)
        server = Server(
            name=name,
            owner_id=current_user.id,
            server_type=server_type,
            server_version=version,
            cpu_cores=resources['cpu'],
            ram_mb=resources['ram'],
            disk_gb=resources['disk'],
            status='creating'
        )
        db.session.add(server)
        db.session.commit()

        # Create in Kubernetes
        try:
            k8s_resources = k8s.create_minecraft_server(k8s_name, {
                'server_type': server_type,
                'server_version': version,
                'cpu_cores': resources['cpu'],
                'ram_mb': resources['ram'],
                'disk_gb': resources['disk']
            })

            # Update database with K8s info
            server.pod_name = k8s_resources['pod_name']
            server.pvc_name = k8s_resources['pvc_name']
            server.service_name = k8s_resources['service_name']
            server.status = 'starting'
            db.session.commit()

            flash(f'Server "{name}" is being created!', 'success')
            return redirect(url_for('servers.dashboard'))

        except Exception as e:
            server.status = 'error'
            db.session.commit()
            flash(f'Error creating server: {str(e)}', 'error')
            return redirect(url_for('servers.create_server'))

    # GET request - show form
    return render_template('servers/create.html')
```

### Dashboard with Real-Time Status

```python
@servers.route('/dashboard')
@login_required
def dashboard():
    # Get user's servers
    user_servers = current_user.servers.all()

    # Update status from Kubernetes
    for server in user_servers:
        if server.pod_name:
            server.status = k8s.get_server_status(server.pod_name).lower()

    db.session.commit()

    # Get resource usage
    usage = current_user.get_resource_usage()

    return render_template('servers/dashboard.html',
                          servers=user_servers,
                          usage=usage)
```

### Server Control Actions

```python
@servers.route('/<int:server_id>/start', methods=['POST'])
@login_required
def start_server(server_id):
    server = Server.query.get_or_404(server_id)

    # Check permission
    if server.owner_id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    try:
        k8s.start_server(server.pod_name)
        server.status = 'starting'
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Server starting'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@servers.route('/<int:server_id>/stop', methods=['POST'])
@login_required
def stop_server(server_id):
    server = Server.query.get_or_404(server_id)

    if server.owner_id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    try:
        k8s.stop_server(server.pod_name)
        server.status = 'stopping'
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Server stopping'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

## 4. WebSocket Console Implementation

### Flask-SocketIO Setup

```python
from flask_socketio import SocketIO, emit, join_room, leave_room
from app import create_app
from app.models import Server
from flask_login import current_user
import threading

app = create_app()
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect', namespace='/console')
def handle_connect():
    if not current_user.is_authenticated:
        return False  # Reject connection
    print(f"User {current_user.email} connected to console")

@socketio.on('join', namespace='/console')
def handle_join(data):
    server_id = data.get('server_id')
    server = Server.query.get(server_id)

    if not server or (server.owner_id != current_user.id and not current_user.is_admin):
        emit('error', {'message': 'Unauthorized'})
        return

    room = f"server_{server_id}"
    join_room(room)

    # Start log streaming in background thread
    def stream_logs_to_socket():
        k8s = KubernetesClient()
        def send_log_line(line):
            socketio.emit('log', {'data': line}, room=room, namespace='/console')

        k8s.stream_logs(server.pod_name, send_log_line)

    thread = threading.Thread(target=stream_logs_to_socket)
    thread.daemon = True
    thread.start()

    emit('joined', {'server_id': server_id})

@socketio.on('command', namespace='/console')
def handle_command(data):
    server_id = data.get('server_id')
    command = data.get('command')

    server = Server.query.get(server_id)
    if not server or (server.owner_id != current_user.id and not current_user.is_admin):
        emit('error', {'message': 'Unauthorized'})
        return

    k8s = KubernetesClient()
    output = k8s.exec_command(server.pod_name, ['rcon-cli', command])

    emit('command_output', {'output': output})

@socketio.on('disconnect', namespace='/console')
def handle_disconnect():
    print(f"User {current_user.email} disconnected")
```

### Console JavaScript Client

```javascript
// app/static/js/console.js
const socket = io('/console');
const serverId = document.getElementById('console').dataset.serverId;
const output = document.getElementById('console-output');
const input = document.getElementById('console-input');

socket.on('connect', function() {
    console.log('Connected to console');
    socket.emit('join', {server_id: serverId});
});

socket.on('log', function(data) {
    appendToConsole(data.data);
});

socket.on('command_output', function(data) {
    appendToConsole(data.output, 'text-green-400');
});

socket.on('error', function(data) {
    appendToConsole('ERROR: ' + data.message, 'text-red-400');
});

input.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        const command = input.value.trim();
        if (command) {
            appendToConsole('> ' + command, 'text-blue-400');
            socket.emit('command', {
                server_id: serverId,
                command: command
            });
            input.value = '';
        }
    }
});

function appendToConsole(text, className = '') {
    const line = document.createElement('div');
    line.textContent = text;
    if (className) line.className = className;
    output.appendChild(line);
    output.scrollTop = output.scrollHeight;
}
```

## 5. File Manager Implementation

### File Listing Endpoint

```python
@files.route('/<int:server_id>/list')
@login_required
def list_files(server_id):
    server = Server.query.get_or_404(server_id)

    # Permission check
    if server.owner_id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    path = request.args.get('path', '/data')

    k8s = KubernetesClient()
    # Execute ls -la in pod
    command = ['ls', '-la', '--time-style=+%Y-%m-%d %H:%M:%S', path]
    output = k8s.exec_command(server.pod_name, command)

    # Parse ls output
    files = parse_ls_output(output)

    return jsonify({'files': files, 'path': path})

def parse_ls_output(output):
    """Parse ls -la output into structured data."""
    lines = output.strip().split('\n')[1:]  # Skip 'total' line
    files = []

    for line in lines:
        parts = line.split(maxsplit=8)
        if len(parts) < 9:
            continue

        perms, _, owner, group, size, date, time, _, name = parts

        files.append({
            'name': name,
            'is_dir': perms.startswith('d'),
            'size': int(size) if not perms.startswith('d') else 0,
            'modified': f"{date} {time}",
            'permissions': perms
        })

    return files
```

### File Read/Edit Endpoints

```python
@files.route('/<int:server_id>/read')
@login_required
def read_file(server_id):
    server = Server.query.get_or_404(server_id)
    if server.owner_id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    filepath = request.args.get('path')
    if not filepath:
        return jsonify({'error': 'Path required'}), 400

    k8s = KubernetesClient()
    content = k8s.exec_command(server.pod_name, ['cat', filepath])

    return jsonify({'content': content, 'path': filepath})

@files.route('/<int:server_id>/write', methods=['POST'])
@login_required
def write_file(server_id):
    server = Server.query.get_or_404(server_id)
    if server.owner_id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    filepath = request.json.get('path')
    content = request.json.get('content')

    k8s = KubernetesClient()
    # Use tee to write file
    command = ['sh', '-c', f'echo "{content}" > {filepath}']
    k8s.exec_command(server.pod_name, command)

    return jsonify({'status': 'success'})
```

## 6. Permission System

### Custom Decorator for Permission Checks

```python
# app/utils/decorators.py
from functools import wraps
from flask import jsonify
from flask_login import current_user
from app.models import Server, ServerPermission

def require_server_permission(permission_name):
    """Decorator to check server-specific permissions."""
    def decorator(f):
        @wraps(f)
        def decorated_function(server_id, *args, **kwargs):
            server = Server.query.get_or_404(server_id)

            # Owner has all permissions
            if server.owner_id == current_user.id or current_user.is_admin:
                return f(server_id, *args, **kwargs)

            # Check sub-user permissions
            perm = ServerPermission.query.filter_by(
                server_id=server_id,
                user_id=current_user.id
            ).first()

            if not perm:
                return jsonify({'error': 'No access to this server'}), 403

            # Check specific permission
            has_perm = getattr(perm, f'can_{permission_name}', False)
            if not has_perm:
                return jsonify({'error': f'Missing permission: {permission_name}'}), 403

            return f(server_id, *args, **kwargs)
        return decorated_function
    return decorator

# Usage:
@servers.route('/<int:server_id>/console')
@login_required
@require_server_permission('console')
def server_console(server_id):
    # User has console permission
    pass
```

## 7. Monitoring Setup

### Prometheus Metrics

```python
from prometheus_flask_exporter import PrometheusMetrics

app = create_app()
metrics = PrometheusMetrics(app)

# Custom metrics
server_creation_counter = Counter(
    'panel_server_creations_total',
    'Total number of servers created'
)

server_deletion_counter = Counter(
    'panel_server_deletions_total',
    'Total number of servers deleted'
)

active_servers_gauge = Gauge(
    'panel_active_servers',
    'Number of currently active servers'
)

# Use in routes:
@servers.route('/create', methods=['POST'])
def create_server():
    # ... creation logic ...
    server_creation_counter.inc()
    active_servers_gauge.set(Server.query.filter_by(status='running').count())
```

This implementation guide provides concrete code examples for each major component. Use these as templates when building the actual system.
