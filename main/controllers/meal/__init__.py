from flask import Blueprint

meal_bp = Blueprint("meal", __name__, url_prefix="/meal")

API_CATEGORY = "Meal"

from main.controllers import authorization_header

from main.controllers.meal.list import meal_list
from main.controllers.meal.requests import (
    meal_requests,
    meal_send_request,
    meal_accept_request,
    meal_ignore_request
)
