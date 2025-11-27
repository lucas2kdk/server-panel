"""
Pytest configuration and fixtures.
"""
import pytest
from app import create_app
from app.models import db, User, Server


@pytest.fixture(scope='session')
def app():
    """Create application for testing."""
    app = create_app('testing')
    return app


@pytest.fixture(scope='function')
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture(scope='function')
def init_database(app):
    """Initialize database for testing."""
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='function')
def test_user(init_database):
    """Create a test user."""
    user = User(email='test@example.com')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture(scope='function')
def admin_user(init_database):
    """Create an admin user."""
    user = User(email='admin@example.com', is_admin=True)
    user.set_password('admin123')
    user.max_cpu_cores = 32
    user.max_ram_gb = 64
    user.max_servers = 20
    db.session.add(user)
    db.session.commit()
    return user
