"""Routes for posts"""
from flask import Blueprint, render_template

posts_bp = Blueprint("posts", __name__)


@posts_bp.route("/")
def index() -> str:
    """Index page"""
    return render_template("posts/index.html")


@posts_bp.route("/categories/")
def categories() -> str:
    """Categories page"""
    return render_template("posts/categories.html")
