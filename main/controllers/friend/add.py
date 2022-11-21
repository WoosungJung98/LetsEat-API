from flask_apispec import use_kwargs, marshal_with, doc
from flask_jwt_extended import jwt_required

from main.controllers.friend import friend_bp, API_CATEGORY, authorization_header
from main.controllers.common.jwt import check_jwt_user
from main.models.common.error import (
    ResponseError,
    ERROR_NONEXISTENT_FRIEND,
    ERROR_FAILED_FRIEND_ADD,
    SUCCESS_ADD_FRIEND
)
from main.models.schema.friend import RequestFriendAddSchema
from main.models.friend import t_friend
from main.models.user import get_user
from main import db


@friend_bp.route("/add", methods=["POST"])
@jwt_required()
@check_jwt_user
@use_kwargs(RequestFriendAddSchema)
@marshal_with(ResponseError)
@doc(tags=[API_CATEGORY],
     summary="Add Friend to Friend List",
     description="Returns the list of friends for the user",
     params=authorization_header)
def friend_add(user, friend_id):
  if not get_user(friend_id):
    return ERROR_NONEXISTENT_FRIEND.get_response()

  try:
    add_friend_query = db.insert(t_friend)\
      .values(user_id=user.user_id, friend_id=friend_id)
    db.session.execute(add_friend_query)
    db.session.commit()
  except:
    return ERROR_FAILED_FRIEND_ADD.get_response()

  return SUCCESS_ADD_FRIEND.get_response()
