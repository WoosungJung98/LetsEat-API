from flask import Blueprint

restaurant_bp = Blueprint("restaurant", __name__, url_prefix="/restaurant")

API_CATEGORY = "Restaurant"

from main.controllers.restaurant.list import restaurant_list
from main.controllers.restaurant.info import restaurant_info
from main.controllers.restaurant.photos import business_photos
