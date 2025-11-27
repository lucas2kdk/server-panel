"""
File management blueprint for browsing and editing server files.
"""
from flask import Blueprint

files = Blueprint('files', __name__)

from app.files import routes  # noqa: F401, E402
