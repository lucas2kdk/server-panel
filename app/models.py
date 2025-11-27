"""
Database models for the game server panel.
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import re

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User model for authentication and resource quota management."""

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

    # Kubernetes namespace for this user
    k8s_namespace = db.Column(db.String(63))  # K8s namespace max length

    # Relationships
    servers = db.relationship('Server', backref='owner', lazy='dynamic',
                            cascade='all, delete-orphan')

    def get_namespace(self) -> str:
        """Get or generate Kubernetes namespace for this user."""
        if not self.k8s_namespace:
            # Generate namespace: user-{id}
            self.k8s_namespace = f"user-{self.id}"
            db.session.commit()
        return self.k8s_namespace

    def set_password(self, password: str) -> None:
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Check if provided password matches the hash."""
        return check_password_hash(self.password_hash, password)

    def get_resource_usage(self) -> dict:
        """Calculate current resource usage across all servers."""
        running_servers = self.servers.filter_by(status='running').all()
        total_cpu = sum(server.cpu_cores for server in running_servers)
        total_ram = sum(server.ram_mb for server in running_servers)
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

    def can_create_server(self, cpu_cores: int, ram_mb: int) -> tuple[bool, str | None]:
        """Check if user has quota for new server."""
        usage = self.get_resource_usage()

        if usage['servers_used'] >= self.max_servers:
            return False, "Server limit reached"

        if usage['cpu_used'] + cpu_cores > self.max_cpu_cores:
            return False, "CPU quota exceeded"

        if usage['ram_used_mb'] + ram_mb > (self.max_ram_gb * 1024):
            return False, "RAM quota exceeded"

        return True, None

    def __repr__(self):
        return f'<User {self.email}>'


class Server(db.Model):
    """Server model representing a game server instance."""

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
    namespace = db.Column(db.String(63))  # K8s namespace
    pod_name = db.Column(db.String(255))
    pvc_name = db.Column(db.String(255))
    service_name = db.Column(db.String(255))

    # Status: creating, starting, running, stopping, stopped, error
    status = db.Column(db.String(20), default='creating')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    permissions = db.relationship('ServerPermission', backref='server', lazy='dynamic',
                                cascade='all, delete-orphan')

    @staticmethod
    def generate_k8s_name(owner_id: int, server_name: str) -> str:
        """Generate Kubernetes-compliant resource name."""
        # K8s names must be lowercase alphanumeric + hyphens, max 63 chars
        safe_name = re.sub(r'[^a-z0-9-]', '', server_name.lower().replace(' ', '-'))
        return f"mc-{owner_id}-{safe_name}"[:63]

    def to_dict(self) -> dict:
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

    def __repr__(self):
        return f'<Server {self.name}>'


class ServerPermission(db.Model):
    """Sub-user permissions for servers."""

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

    def __repr__(self):
        return f'<ServerPermission user={self.user_id} server={self.server_id}>'


class ServerTemplate(db.Model):
    """Server templates (eggs) for quick deployment."""

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

    def __repr__(self):
        return f'<ServerTemplate {self.name}>'


class AuditLog(db.Model):
    """Audit log for tracking user actions."""

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

    def __repr__(self):
        return f'<AuditLog {self.action} by user={self.user_id}>'
