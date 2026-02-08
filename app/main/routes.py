from flask import render_template
from app.main import bp

@bp.route('/')
def index():
    """Landing page with role selection."""
    return render_template('index.html')
