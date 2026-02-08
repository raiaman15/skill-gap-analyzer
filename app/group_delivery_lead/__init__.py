from flask import Blueprint

bp = Blueprint('group_delivery_lead', __name__, url_prefix='/group-delivery-lead')

from app.group_delivery_lead import routes
