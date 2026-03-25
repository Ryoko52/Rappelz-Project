"""Entry point for the Flask application."""
import os
from app import create_app

if __name__ == '__main__':
    app = create_app(os.environ.get('FLASK_ENV', 'development'))
    app.run(host='127.0.0.1', port=5000, debug=True)
