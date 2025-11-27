"""
Unit tests for authentication routes.
"""
import pytest


def test_login_page_loads(client):
    """Test login page is accessible."""
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Login' in response.data


def test_register_page_loads(client):
    """Test register page is accessible."""
    response = client.get('/auth/register')
    assert response.status_code == 200
    assert b'Register' in response.data


def test_successful_registration(client, init_database):
    """Test user can register successfully."""
    response = client.post('/auth/register', data={
        'email': 'newuser@example.com',
        'password': 'password123',
        'password_confirm': 'password123'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Registration successful' in response.data


def test_duplicate_email_registration(client, test_user, init_database):
    """Test registration fails with duplicate email."""
    response = client.post('/auth/register', data={
        'email': test_user.email,
        'password': 'password123',
        'password_confirm': 'password123'
    }, follow_redirects=True)

    assert b'Email already registered' in response.data


def test_successful_login(client, test_user, init_database):
    """Test user can login successfully."""
    response = client.post('/auth/login', data={
        'email': test_user.email,
        'password': 'password123'
    }, follow_redirects=True)

    assert response.status_code == 200


def test_failed_login_wrong_password(client, test_user, init_database):
    """Test login fails with wrong password."""
    response = client.post('/auth/login', data={
        'email': test_user.email,
        'password': 'wrongpassword'
    }, follow_redirects=True)

    assert b'Invalid email or password' in response.data


def test_failed_login_nonexistent_user(client, init_database):
    """Test login fails with nonexistent user."""
    response = client.post('/auth/login', data={
        'email': 'nonexistent@example.com',
        'password': 'password123'
    }, follow_redirects=True)

    assert b'Invalid email or password' in response.data
