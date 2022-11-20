from flask_apispec import use_kwargs, marshal_with, doc
from flask_jwt_extended import jwt_required

from main.controllers.friend import friend_bp, API_CATEGORY, authorization_header
from main.controllers.common.jwt import check_jwt_user
from main.models.common.error import ResponseError
from main.models.schema.friend import (
    RequestFriendListSchema,
    ResponseFriendListSchema
)
from main.models.friend import t_friend
from main.models.user import t_user
from main import db
from sqlalchemy import func, nullslast

FRIEND_LIST_LENGTH = 30


@friend_bp.route("/list", methods=["GET"])
@jwt_required()
@check_jwt_user
@use_kwargs(RequestFriendListSchema, location="query")
@marshal_with(ResponseError)
@marshal_with(ResponseFriendListSchema, code=200)
@doc(tags=[API_CATEGORY],
     summary="Get Friend List",
     description="Returns the list of friends for the user",
     params=authorization_header)
def friend_list(user, friend_name=None):
  query = db.select(t_friend.c.friend_id, t_user.c.user_name, t_user.c.profile_photo)\
            .join(t_user, t_friend.c.friend_id == t_user.c.user_id)\
            .where(t_friend.c.user_id == user.user_id)
  if friend_name:
    query = query.where(func.lower(t_user.c.user_name).like(f"%{friend_name.strip().lower()}%"))
  query = query.order_by(nullslast(t_friend.c.viewed_at.desc()))\
               .limit(FRIEND_LIST_LENGTH)
  
  result = db.session.execute(query)
  friend_results={}
  friend_results["friend_list"] = [{
    "friend_id": friend.friend_id,
    "user_name": friend.user_name,
    "profile_photo": friend.profile_photo,
  } for friend in result]

  return friend_results
