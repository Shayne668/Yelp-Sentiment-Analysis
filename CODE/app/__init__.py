# app/__init__.py
from flask import Flask
from .data_loader import cache

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')

    # Import and register blueprints
    from .routes import wordcloud_bp
    app.register_blueprint(wordcloud_bp)

    # Initialize the cache extension
    cache.init_app(app)

    return app