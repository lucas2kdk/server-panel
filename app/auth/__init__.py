"""
Authentication blueprint for user login, registration, and session management.
"""
from flask import Blueprint

auth = Blueprint('auth', __name__)

from app.auth import routes  # noqa: F401, E402
