from flask_apispec import marshal_with, doc
from flask_jwt_extended import jwt_required

from main.controllers.friend import friend_bp, API_CATEGORY, authorization_header
from main.controllers.common.jwt import check_jwt_user
from main.models.common.error import ResponseError
from main.models.schema.friend import ResponseFriendRequestListSchema
from main.models.friend_request import t_friend_request
from main import db

FRIEND_REQUEST_LIST_LENGTH = 10


@friend_bp.route("/requests", methods=["GET"])
@jwt_required()
@check_jwt_user
@marshal_with(ResponseError)
@marshal_with(ResponseFriendRequestListSchema, code=200)
@doc(tags=[API_CATEGORY],
     summary="Get Friend List",
     description="Returns the list of friends for the user",
     params=authorization_header)
def friend_requests(user):
  query = db\
    .select(
      t_friend_request.c.user_id,
      t_friend_request.c.created_at)\
    .where(t_friend_request.c.friend_id == user.user_id)
  query = query.limit(FRIEND_REQUEST_LIST_LENGTH)
  
  result = db.session.execute(query)
  friend_request_results={}
  friend_request_results["friend_request_list"] = [{
    "user_id": friend_request.user_id,
    "created_at": friend_request.created_at,
  } for friend_request in result]

  return friend_request_results
