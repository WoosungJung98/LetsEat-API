from flask_apispec import use_kwargs, marshal_with, doc
from flask_jwt_extended import jwt_required

from main.controllers.friend import friend_bp, API_CATEGORY, authorization_header
from main.controllers.common.jwt import check_jwt_user
from main.models.common.error import ResponseError
from main.models.friend import t_friend
from main.models.schema.friend import (
    RequestFriendMutualSchema,
    ResponseFriendMutualSchema
)
from main import db


@friend_bp.route("/mutual", methods=["GET"])
@jwt_required()
@check_jwt_user
@use_kwargs(RequestFriendMutualSchema, location="query")
@marshal_with(ResponseError)
@marshal_with(ResponseFriendMutualSchema, code=200)
@doc(tags=[API_CATEGORY],
     summary="Checks mutuality of friendship",
     description="Checks whether given friend is mutual friends with the user",
     params=authorization_header)
def friend_mutual(user, friend_id):
  friend_query = db.session.query(t_friend.c.user_id)\
                   .filter(t_friend.c.user_id == user.user_id)\
                   .filter(t_friend.c.friend_id == friend_id)
  reverse_query = db.session.query(t_friend.c.user_id)\
                    .filter(t_friend.c.user_id == friend_id)\
                    .filter(t_friend.c.friend_id == user.user_id)
  result = friend_query.union_all(reverse_query).count()

  return {"is_mutual": result == 2}
