from flask import Blueprint #type: ignore

bp = Blueprint('main', __name__)

from app.main import routes
