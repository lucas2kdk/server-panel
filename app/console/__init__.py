"""
Console blueprint for WebSocket-based server console access.
"""
from flask import Blueprint

console = Blueprint('console', __name__)

from app.console import routes  # noqa: F401, E402
