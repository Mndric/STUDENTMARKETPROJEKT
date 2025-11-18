from flask import Blueprint

ads_bp = Blueprint('ads', __name__)

from app.ads import routes
