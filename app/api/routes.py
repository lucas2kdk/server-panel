"""
REST API routes for programmatic access.
"""
from flask import jsonify, request
from flask_login import login_required, current_user
from app.api import api
from app.models import Server


@api.route('/servers', methods=['GET'])
@login_required
def list_servers():
    """List all servers for the current user."""
    servers = current_user.servers.all()
    return jsonify({
        'servers': [server.to_dict() for server in servers]
    })


@api.route('/servers/<int:server_id>', methods=['GET'])
@login_required
def get_server(server_id):
    """Get details of a specific server."""
    server = Server.query.get_or_404(server_id)

    # Check permission
    if server.owner_id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    return jsonify(server.to_dict())


@api.route('/user/usage', methods=['GET'])
@login_required
def get_usage():
    """Get current user's resource usage."""
    usage = current_user.get_resource_usage()
    return jsonify(usage)


@api.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'server-panel-api'
    })
