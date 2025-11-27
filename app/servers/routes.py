"""
Server management routes for CRUD operations on game servers.
"""
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.servers import servers
from app.models import db, Server
from app.servers.kubernetes_client import KubernetesClient
from app.config import Config
import logging

logger = logging.getLogger(__name__)
k8s = KubernetesClient()


@servers.route('/dashboard')
@login_required
def dashboard():
    """Display user's server dashboard."""
    # Get user's servers
    user_servers = current_user.servers.all()

    # Update status from Kubernetes
    for server in user_servers:
        if server.pod_name:
            try:
                status = k8s.get_server_status(server.pod_name).lower()
                server.status = status
            except Exception as e:
                logger.error(f"Error updating status for server {server.id}: {e}")
                server.status = 'error'

    db.session.commit()

    # Get resource usage
    usage = current_user.get_resource_usage()

    return render_template('servers/dashboard.html',
                          servers=user_servers,
                          usage=usage)


@servers.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create a new server."""
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form.get('name', '').strip()
            server_type = request.form.get('type', 'paper')
            version = request.form.get('version', '1.20.1')
            plan = request.form.get('plan', 'small')

            # Validation
            if not name:
                flash('Server name is required.', 'error')
                return redirect(url_for('servers.create'))

            # Get resource plan
            plans = Config.RESOURCE_PLANS
            if plan not in plans:
                flash('Invalid resource plan.', 'error')
                return redirect(url_for('servers.create'))

            resources = plans[plan]

            # Check quota
            can_create, error = current_user.can_create_server(
                resources['cpu_cores'],
                resources['ram_mb']
            )
            if not can_create:
                flash(f'Cannot create server: {error}', 'error')
                return redirect(url_for('servers.create'))

            # Generate Kubernetes name
            k8s_name = Server.generate_k8s_name(current_user.id, name)

            # Create database record
            server = Server(
                name=name,
                owner_id=current_user.id,
                server_type=server_type,
                server_version=version,
                cpu_cores=resources['cpu_cores'],
                ram_mb=resources['ram_mb'],
                disk_gb=resources['disk_gb'],
                status='creating'
            )
            db.session.add(server)
            db.session.commit()

            # Create in Kubernetes
            try:
                k8s_resources = k8s.create_minecraft_server(k8s_name, {
                    'server_type': server_type,
                    'server_version': version,
                    'cpu_cores': resources['cpu_cores'],
                    'ram_mb': resources['ram_mb'],
                    'disk_gb': resources['disk_gb']
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
                logger.error(f"Failed to create Kubernetes resources: {e}")
                server.status = 'error'
                db.session.commit()
                flash(f'Error creating server: {str(e)}', 'error')
                return redirect(url_for('servers.create'))

        except Exception as e:
            logger.error(f"Error in server creation: {e}")
            db.session.rollback()
            flash(f'Error creating server: {str(e)}', 'error')
            return redirect(url_for('servers.create'))

    # GET request - show form
    return render_template('servers/create.html', plans=Config.RESOURCE_PLANS)


@servers.route('/<int:server_id>')
@login_required
def detail(server_id):
    """View server details."""
    server = Server.query.get_or_404(server_id)

    # Check permission
    if server.owner_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to view this server.', 'error')
        return redirect(url_for('servers.dashboard'))

    # Update status
    if server.pod_name:
        try:
            status = k8s.get_server_status(server.pod_name).lower()
            server.status = status
            db.session.commit()
        except Exception as e:
            logger.error(f"Error updating server status: {e}")

    return render_template('servers/detail.html', server=server)


@servers.route('/<int:server_id>/start', methods=['POST'])
@login_required
def start(server_id):
    """Start a server."""
    server = Server.query.get_or_404(server_id)

    # Check permission
    if server.owner_id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    try:
        # Extract server name from pod_name (remove -0 suffix)
        server_name = server.pod_name.rsplit('-', 1)[0] if server.pod_name else None
        if not server_name:
            return jsonify({'error': 'Invalid server configuration'}), 400

        k8s.start_server(server_name)
        server.status = 'starting'
        db.session.commit()

        return jsonify({'status': 'success', 'message': 'Server starting'})

    except Exception as e:
        logger.error(f"Error starting server {server_id}: {e}")
        return jsonify({'error': str(e)}), 500


@servers.route('/<int:server_id>/stop', methods=['POST'])
@login_required
def stop(server_id):
    """Stop a server."""
    server = Server.query.get_or_404(server_id)

    # Check permission
    if server.owner_id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    try:
        # Extract server name from pod_name
        server_name = server.pod_name.rsplit('-', 1)[0] if server.pod_name else None
        if not server_name:
            return jsonify({'error': 'Invalid server configuration'}), 400

        k8s.stop_server(server_name)
        server.status = 'stopping'
        db.session.commit()

        return jsonify({'status': 'success', 'message': 'Server stopping'})

    except Exception as e:
        logger.error(f"Error stopping server {server_id}: {e}")
        return jsonify({'error': str(e)}), 500


@servers.route('/<int:server_id>/restart', methods=['POST'])
@login_required
def restart(server_id):
    """Restart a server."""
    server = Server.query.get_or_404(server_id)

    # Check permission
    if server.owner_id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    try:
        server_name = server.pod_name.rsplit('-', 1)[0] if server.pod_name else None
        if not server_name:
            return jsonify({'error': 'Invalid server configuration'}), 400

        # Stop then start
        k8s.stop_server(server_name)
        k8s.start_server(server_name)
        server.status = 'starting'
        db.session.commit()

        return jsonify({'status': 'success', 'message': 'Server restarting'})

    except Exception as e:
        logger.error(f"Error restarting server {server_id}: {e}")
        return jsonify({'error': str(e)}), 500


@servers.route('/<int:server_id>/delete', methods=['POST'])
@login_required
def delete(server_id):
    """Delete a server."""
    server = Server.query.get_or_404(server_id)

    # Check permission (only owner can delete)
    if server.owner_id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    try:
        server_name = server.pod_name.rsplit('-', 1)[0] if server.pod_name else None

        # Delete from Kubernetes
        if server_name:
            try:
                k8s.delete_server(server_name)
            except Exception as e:
                logger.error(f"Error deleting Kubernetes resources: {e}")
                # Continue with database deletion even if K8s deletion fails

        # Delete from database
        db.session.delete(server)
        db.session.commit()

        flash(f'Server "{server.name}" has been deleted.', 'success')
        return jsonify({'status': 'success', 'message': 'Server deleted'})

    except Exception as e:
        logger.error(f"Error deleting server {server_id}: {e}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
