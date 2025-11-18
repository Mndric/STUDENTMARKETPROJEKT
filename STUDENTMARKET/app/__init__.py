from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_principal import Principal, Permission, RoleNeed
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Initialize extensions
mongo = PyMongo()
login_manager = LoginManager()
principals = Principal()
mail = Mail()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Define permissions
admin_permission = Permission(RoleNeed('admin'))


def create_app(config_name='default'):
    """Create and configure the Flask application"""
    app = Flask(__name__, instance_relative_config=False)
    
    # Load configuration
    from config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    mongo.init_app(app)
    login_manager.init_app(app)
    principals.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)
    
    # Configure Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    from app.auth import auth_bp
    from app.main import main_bp
    from app.ads import ads_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(ads_bp, url_prefix='/ads')
    
    # User loader for Flask-Login
    from app.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(user_id)
    
    # Identity loader for Flask-Principal
    from flask_principal import identity_loaded, UserNeed
    from flask_login import current_user
    
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        identity.user = current_user
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(str(current_user.id)))
        if hasattr(current_user, 'is_admin') and current_user.is_admin:
            identity.provides.add(RoleNeed('admin'))
    
    # Register error handlers
    register_error_handlers(app)
    
    # Security headers
    @app.after_request
    def set_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        return response
    
    # Context processor for templates
    @app.context_processor
    def inject_now():
        from datetime import datetime
        return {'current_year': datetime.utcnow().year}
    
    # Create admin user if configured
    with app.app_context():
        create_admin_user()
    
    return app


def register_error_handlers(app):
    """Register error handlers"""
    from flask import render_template
    
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(429)
    def rate_limited(e):
        return render_template('errors/429.html'), 429
    
    @app.errorhandler(500)
    def internal_error(e):
        return render_template('errors/500.html'), 500


def create_admin_user():
    """Create initial admin user if configured"""
    from app.models import User
    from flask import current_app
    
    admin_email = current_app.config.get('ADMIN_EMAIL')
    admin_password = current_app.config.get('ADMIN_PASSWORD')
    admin_name = current_app.config.get('ADMIN_USERNAME', 'Admin')
    
    if not admin_email or not admin_password:
        return
    
    # Check if mongo.db is available
    try:
        from app import mongo
        if getattr(mongo, 'db', None) is None:
            print("Warning: MongoDB not initialized. Skipping admin creation.")
            return
    except Exception as e:
        print(f"Warning: Error checking MongoDB: {e}. Skipping admin creation.")
        return
    
    # Check if admin user already exists
    try:
        existing = User.get_by_email(admin_email)
        if not existing:
            User.create_admin(admin_name, admin_email, admin_password)
            print(f"Admin user '{admin_name}' created with email: {admin_email}")
    except Exception as e:
        print(f"Warning: Could not create admin user: {e}")
