from flask_apispec import marshal_with, doc
from flask_jwt_extended import jwt_required

from main.controllers.friend import friend_bp, API_CATEGORY, authorization_header
from main.controllers.common.jwt import check_jwt_user
from main.models.common.error import ResponseError
from main.models.schema.friend import ResponseFriendRequestListSchema
from main.models.friend_request import t_friend_request
from main.models.user import t_user
from main import db
from sqlalchemy import extract, func

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
      t_user.c.user_name,
      func.trunc((extract("epoch", func.now()) - extract("epoch", t_friend_request.c.created_at)) / 60).label("time_diff"))\
    .join(t_user, t_friend_request.c.user_id == t_user.c.user_id)\
    .where(t_friend_request.c.friend_id == user.user_id)\
    .where(t_friend_request.c.ignored_at == None)\
    .order_by(t_friend_request.c.created_at.desc())\
    .limit(FRIEND_REQUEST_LIST_LENGTH)
  
  result = db.session.execute(query)
  friend_request_results={}
  friend_request_results["friend_request_list"] = [{
    "user_name": friend_request.user_name,
    "time_diff": friend_request.time_diff,
  } for friend_request in result]

  return friend_request_results
