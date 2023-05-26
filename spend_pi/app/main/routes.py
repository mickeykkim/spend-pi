"""Routes for spend_pi"""
from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index() -> str:
    """Index page"""
    return render_template("index.html")
