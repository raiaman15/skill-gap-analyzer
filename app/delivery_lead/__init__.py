from flask import Blueprint

bp = Blueprint('delivery_lead', __name__, url_prefix='/delivery-lead')

from app.delivery_lead import routes
