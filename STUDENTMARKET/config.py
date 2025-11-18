import os
from dotenv import load_dotenv

load_dotenv()

# Ensure MongoDB URI contains database name for Flask-PyMongo
try:
    from pymongo import uri_parser
except Exception:
    uri_parser = None


class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # MongoDB Configuration
    _mongo_uri_env = os.environ.get('MONGODB_URI')
    _mongo_db_env = os.environ.get('MONGODB_DB', 'student_market')
    
    if _mongo_uri_env:
        # Ensure URI includes database name
        database_name = None
        if uri_parser is not None:
            try:
                parsed = uri_parser.parse_uri(_mongo_uri_env)
                database_name = parsed.get('database')
            except Exception:
                database_name = None
        
        if database_name:
            MONGO_URI = _mongo_uri_env
        else:
            MONGO_URI = _mongo_uri_env.rstrip('/') + '/' + _mongo_db_env
    else:
        MONGO_URI = f'mongodb://localhost:27017/{_mongo_db_env}'
    
    MONGO_DBNAME = _mongo_db_env
    
    # Email Configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 465))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'False') == 'True'
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'True') == 'True'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@studentmarket.local')
    MAIL_TIMEOUT = int(os.environ.get('MAIL_TIMEOUT', 10))
    
    # Security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    REMEMBER_COOKIE_DURATION = 7  # days
    
    # Pagination
    ITEMS_PER_PAGE = 12
    
    # Admin User
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@studentmarket.local')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
