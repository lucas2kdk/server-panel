"""
Configuration classes for the Flask application.
"""
import os
from datetime import timedelta


class Config:
    """Base configuration class."""

    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:postgres@localhost:5432/serverpanel'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }

    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False  # Set True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # Kubernetes
    K8S_NAMESPACE = os.environ.get('K8S_NAMESPACE') or 'game-servers'
    K8S_IN_CLUSTER = os.environ.get('K8S_IN_CLUSTER', 'false').lower() == 'true'

    # Resource defaults
    DEFAULT_CPU_QUOTA = 8  # CPU cores
    DEFAULT_RAM_QUOTA = 16  # GB
    DEFAULT_MAX_SERVERS = 5

    # Resource plans
    RESOURCE_PLANS = {
        'small': {
            'cpu_cores': 1,
            'ram_mb': 2048,
            'disk_gb': 10
        },
        'medium': {
            'cpu_cores': 2,
            'ram_mb': 4096,
            'disk_gb': 20
        },
        'large': {
            'cpu_cores': 4,
            'ram_mb': 8192,
            'disk_gb': 40
        }
    }


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
