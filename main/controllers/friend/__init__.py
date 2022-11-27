from flask import Blueprint

friend_bp = Blueprint("friend", __name__, url_prefix="/friend")

API_CATEGORY = "Friend"

from main.controllers import authorization_header

from main.controllers.friend.list import friend_list
from main.controllers.friend.mutual import friend_mutual
from main.controllers.friend.add import friend_add
