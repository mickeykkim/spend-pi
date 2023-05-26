"""Entrypoint for main app"""
from typing import Type

from flask import Flask

from spend_pi.config import Config


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
    from spend_pi.app.main.routes import main_bp
    from spend_pi.app.posts.routes import posts_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(posts_bp, url_prefix="/posts")

    return app
