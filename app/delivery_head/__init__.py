from flask import Blueprint

bp = Blueprint('delivery_head', __name__)

from app.delivery_head import routes
