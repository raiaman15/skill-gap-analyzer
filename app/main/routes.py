from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Landing page with role selection."""
    return render_template('index.html')
