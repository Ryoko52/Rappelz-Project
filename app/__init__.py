from flask import Flask

def create_app(config_name='development'):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    if config_name == 'development':
        app.config['DEBUG'] = True
    elif config_name == 'production':
        app.config['DEBUG'] = False
    
    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app
