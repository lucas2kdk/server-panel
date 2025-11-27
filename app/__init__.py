"""
Flask application factory and initialization.
"""
from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from app.config import config
from app.models import db, User

login_manager = LoginManager()
migrate = Migrate()


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login."""
    return User.query.get(int(user_id))


def create_app(config_name='default'):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    # Register blueprints
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from app.servers import servers as servers_blueprint
    app.register_blueprint(servers_blueprint, url_prefix='/servers')

    from app.console import console as console_blueprint
    app.register_blueprint(console_blueprint, url_prefix='/console')

    from app.files import files as files_blueprint
    app.register_blueprint(files_blueprint, url_prefix='/files')

    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    # Root route
    @app.route('/')
    def index():
        """Landing page."""
        return render_template('index.html')

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        """Handle 404 errors."""
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(e):
        """Handle 500 errors."""
        db.session.rollback()
        return render_template('errors/500.html'), 500

    # Flask CLI commands for database migrations
    @app.cli.command('db-upgrade')
    def db_upgrade():
        """Apply database migrations."""
        from flask_migrate import upgrade
        upgrade()
        print("✓ Database migrations applied successfully!")

    @app.cli.command('db-init')
    def db_init():
        """Initialize database (create all tables)."""
        db.create_all()
        print("✓ Database initialized!")

    return app
