"""
File management routes for browsing and editing server files.
"""
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.files import files
from app.models import Server
from app.servers.kubernetes_client import KubernetesClient
import logging
import os

logger = logging.getLogger(__name__)
k8s = KubernetesClient()


@files.route('/<int:server_id>/browser')
@login_required
def browser(server_id):
    """File browser interface."""
    server = Server.query.get_or_404(server_id)

    # Check permission
    if server.owner_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to access this server files.', 'error')
        return redirect(url_for('servers.dashboard'))

    return render_template('files/browser.html', server=server)


@files.route('/<int:server_id>/list')
@login_required
def list_files(server_id):
    """List files in a directory (AJAX endpoint)."""
    server = Server.query.get_or_404(server_id)

    # Check permission
    if server.owner_id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    path = request.args.get('path', '/data')

    # Security: prevent path traversal
    if '..' in path:
        return jsonify({'error': 'Invalid path'}), 400

    try:
        output = k8s.list_files(server.pod_name, path, server.namespace)
        files_list = parse_ls_output(output)
        return jsonify({'files': files_list, 'path': path})

    except Exception as e:
        logger.error(f"Error listing files for server {server_id}: {e}")
        return jsonify({'error': str(e)}), 500


@files.route('/<int:server_id>/read')
@login_required
def read_file(server_id):
    """Read a file (AJAX endpoint)."""
    server = Server.query.get_or_404(server_id)

    # Check permission
    if server.owner_id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    filepath = request.args.get('path')
    if not filepath:
        return jsonify({'error': 'Path required'}), 400

    # Security: prevent path traversal
    if '..' in filepath:
        return jsonify({'error': 'Invalid path'}), 400

    try:
        content = k8s.read_file(server.pod_name, filepath, server.namespace)
        return jsonify({'content': content, 'path': filepath})

    except Exception as e:
        logger.error(f"Error reading file for server {server_id}: {e}")
        return jsonify({'error': str(e)}), 500


@files.route('/<int:server_id>/write', methods=['POST'])
@login_required
def write_file(server_id):
    """Write to a file (AJAX endpoint)."""
    server = Server.query.get_or_404(server_id)

    # Check permission
    if server.owner_id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    filepath = data.get('path')
    content = data.get('content')

    if not filepath or content is None:
        return jsonify({'error': 'Path and content required'}), 400

    # Security: prevent path traversal
    if '..' in filepath:
        return jsonify({'error': 'Invalid path'}), 400

    try:
        k8s.write_file(server.pod_name, filepath, content, server.namespace)
        return jsonify({'status': 'success', 'message': 'File saved'})

    except Exception as e:
        logger.error(f"Error writing file for server {server_id}: {e}")
        return jsonify({'error': str(e)}), 500


def parse_ls_output(output: str) -> list:
    """Parse ls -la output into structured data."""
    lines = output.strip().split('\n')
    if len(lines) <= 1:
        return []

    files_list = []
    for line in lines[1:]:  # Skip 'total' line
        parts = line.split(maxsplit=8)
        if len(parts) < 9:
            continue

        perms, _, owner, group, size, date, time, _, name = parts

        # Skip . and ..
        if name in ['.', '..']:
            continue

        files_list.append({
            'name': name,
            'is_dir': perms.startswith('d'),
            'size': int(size) if not perms.startswith('d') else 0,
            'modified': f"{date} {time}",
            'permissions': perms
        })

    return files_list
