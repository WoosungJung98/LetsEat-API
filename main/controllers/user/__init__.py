from flask import Blueprint

user_bp = Blueprint("user", __name__, url_prefix="/user")

API_CATEGORY = "User"

from main.controllers import authorization_header, FACEYELP_API_CACHE

from main.controllers.user.login import (
    user_login,
    user_refresh,
    user_logout,
    user_change_password,
)
from main.controllers.user.info import user_info
from main.controllers.user.list import user_list
from main.controllers.user.create import (
    user_create,
    user_verify_email
)
