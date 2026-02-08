from flask import Blueprint

bp = Blueprint('group_delivery_lead', __name__)

from app.group_delivery_lead import routes
