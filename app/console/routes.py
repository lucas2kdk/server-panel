"""
Console routes for WebSocket-based server console access.
"""
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.console import console
from app.models import Server
from app.servers.kubernetes_client import KubernetesClient
import logging

logger = logging.getLogger(__name__)
k8s = KubernetesClient()


@console.route('/<int:server_id>')
@login_required
def view(server_id):
    """View server console."""
    server = Server.query.get_or_404(server_id)

    # Check permission
    if server.owner_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to access this server console.', 'error')
        return redirect(url_for('servers.dashboard'))

    # Get recent logs
    try:
        logs = k8s.get_server_logs(server.pod_name, tail_lines=100) if server.pod_name else "Server not running."
    except Exception as e:
        logger.error(f"Error fetching logs for server {server_id}: {e}")
        logs = f"Error fetching logs: {str(e)}"

    return render_template('console/console.html', server=server, logs=logs)


@console.route('/<int:server_id>/logs')
@login_required
def logs(server_id):
    """Get server logs (AJAX endpoint)."""
    server = Server.query.get_or_404(server_id)

    # Check permission
    if server.owner_id != current_user.id and not current_user.is_admin:
        return {'error': 'Unauthorized'}, 403

    try:
        logs = k8s.get_server_logs(server.pod_name, tail_lines=100) if server.pod_name else "Server not running."
        return {'logs': logs}
    except Exception as e:
        logger.error(f"Error fetching logs for server {server_id}: {e}")
        return {'error': str(e)}, 500
