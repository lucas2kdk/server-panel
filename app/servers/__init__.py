"""
Server management blueprint for CRUD operations on game servers.
"""
from flask import Blueprint

servers = Blueprint('servers', __name__)

from app.servers import routes  # noqa: F401, E402
