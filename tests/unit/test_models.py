"""
Unit tests for database models.
"""
import pytest
from app.models import User, Server


def test_user_password_hashing(test_user):
    """Test password hashing works correctly."""
    assert test_user.password_hash is not None
    assert test_user.password_hash != 'password123'
    assert test_user.check_password('password123')
    assert not test_user.check_password('wrongpassword')


def test_user_resource_usage(test_user, init_database):
    """Test resource usage calculation."""
    usage = test_user.get_resource_usage()
    assert usage['cpu_used'] == 0
    assert usage['ram_used_mb'] == 0
    assert usage['servers_used'] == 0
    assert usage['cpu_max'] == test_user.max_cpu_cores
    assert usage['ram_max_mb'] == test_user.max_ram_gb * 1024


def test_user_can_create_server(test_user):
    """Test quota checking for server creation."""
    can_create, error = test_user.can_create_server(2, 4096)
    assert can_create is True
    assert error is None

    # Exceed server limit
    test_user.max_servers = 0
    can_create, error = test_user.can_create_server(2, 4096)
    assert can_create is False
    assert 'Server limit' in error


def test_server_k8s_name_generation():
    """Test Kubernetes name generation."""
    name = Server.generate_k8s_name(1, "My Awesome Server!")
    assert name.startswith('mc-1-')
    assert name.islower()
    assert ' ' not in name
    assert '!' not in name
    assert len(name) <= 63


def test_server_to_dict(test_user, init_database):
    """Test server serialization."""
    server = Server(
        name='Test Server',
        owner_id=test_user.id,
        server_type='paper',
        server_version='1.20.1',
        cpu_cores=2,
        ram_mb=4096,
        disk_gb=20
    )
    init_database.session.add(server)
    init_database.session.commit()

    server_dict = server.to_dict()
    assert server_dict['name'] == 'Test Server'
    assert server_dict['type'] == 'paper'
    assert server_dict['resources']['cpu'] == 2
    assert server_dict['resources']['ram_mb'] == 4096
