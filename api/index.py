"""Entrypoint for main app"""
from typing import Type

from flask import Flask

from api.config import Config


def create_app(config_class: Type[Config] = Config) -> Flask:
    """
    Creates an app instance

    Params:
        config_class: A class with configuration parameters

    Returns:
        app: Flask app instance
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here

    # Register blueprints here
    from api.main.routes import main_bp
    from api.posts.routes import posts_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(posts_bp, url_prefix="/posts")

    return app
