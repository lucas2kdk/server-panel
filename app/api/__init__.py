"""
REST API blueprint for programmatic access to server panel.
"""
from flask import Blueprint

api = Blueprint('api', __name__)

from app.api import routes  # noqa: F401, E402
