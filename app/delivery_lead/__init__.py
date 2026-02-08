from flask import Blueprint

bp = Blueprint('delivery_lead', __name__)

from app.delivery_lead import routes
