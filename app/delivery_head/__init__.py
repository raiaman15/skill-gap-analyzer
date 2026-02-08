from flask import Blueprint

bp = Blueprint('delivery_head', __name__, url_prefix='/delivery-head')

from app.delivery_head import routes
