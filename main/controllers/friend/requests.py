from flask_apispec import use_kwargs, marshal_with, doc
from flask_jwt_extended import jwt_required

from main.controllers.friend import friend_bp, API_CATEGORY, authorization_header
from main.controllers.common.jwt import check_jwt_user
from main.models.common.error import (
    ResponseError,
    ERROR_NONEXISTENT_FRIEND_REQUEST,
    SUCCESS_ACCEPT_FRIEND_REQUEST,
    SUCCESS_IGNORE_FRIEND_REQUEST
)
from main.models.schema.friend import (
    ResponseFriendRequestListSchema,
    RequestFriendAcceptRequestSchema,
    RequestFriendIgnoreRequestSchema
)
from main.models.friend_request import t_friend_request
from main.models.user import t_user
from main.models.friend import t_friend
from main import db
from sqlalchemy import extract, func
from sqlalchemy.dialects.postgresql import insert

FRIEND_REQUEST_LIST_LENGTH = 10


@friend_bp.route("/requests", methods=["GET"])
@jwt_required()
@check_jwt_user
@marshal_with(ResponseError)
@marshal_with(ResponseFriendRequestListSchema, code=200)
@doc(tags=[API_CATEGORY],
     summary="Get Friend Request List",
     description="Returns the list of actionable friend requests for given user",
     params=authorization_header)
def friend_requests(user):
  query = db\
    .select(
      t_friend_request.c.friend_request_id,
      t_user.c.user_name,
      func.trunc((extract("epoch", func.now()) - extract("epoch", t_friend_request.c.created_at)) / 60).label("time_diff"))\
    .join(t_user, t_friend_request.c.user_id == t_user.c.user_id)\
    .where(t_friend_request.c.friend_id == user.user_id)\
    .where(t_friend_request.c.accepted_at == None)\
    .where(t_friend_request.c.ignored_at == None)\
    .order_by(t_friend_request.c.created_at.desc())\
    .limit(FRIEND_REQUEST_LIST_LENGTH)
  
  result = db.session.execute(query)
  friend_request_results={}
  friend_request_results["friend_request_list"] = [{
    "friend_request_id": friend_request.friend_request_id,
    "user_name": friend_request.user_name,
    "time_diff": friend_request.time_diff,
  } for friend_request in result]

  return friend_request_results


@friend_bp.route("/accept-request", methods=["POST"])
@jwt_required()
@check_jwt_user
@use_kwargs(RequestFriendAcceptRequestSchema)
@marshal_with(ResponseError)
@doc(tags=[API_CATEGORY],
     summary="Accept Friend Request",
     description="Accepts a friend request specified via friend request ID",
     params=authorization_header)
def friend_accept_request(user, friend_request_id):
  friend_request = db.session.query(t_friend_request.c.user_id, t_friend_request.c.friend_id)\
    .filter(t_friend_request.c.friend_request_id == friend_request_id)\
    .scalar()
  if not friend_request:
    return ERROR_NONEXISTENT_FRIEND_REQUEST.get_response()

  insert_stmt = insert(t_friend).values({
    t_friend.c.user_id: friend_request.user_id,
    t_friend.c.friend_id: friend_request.friend_id
  })
  do_nothing_stmt = insert_stmt.on_conflict_do_nothing(
      index_elements=[t_friend.c.user_id, t_friend.c.friend_id]
  )
  db.session.execute(do_nothing_stmt)
  db.session.commit()

  insert_reverse_stmt = insert(t_friend).values({
    t_friend.c.user_id: friend_request.friend_id,
    t_friend.c.friend_id: friend_request.user_id
  })
  do_nothing_reverse_stmt = insert_reverse_stmt.on_conflict_do_nothing(
      index_elements=[t_friend.c.user_id, t_friend.c.friend_id]
  )
  db.session.execute(do_nothing_reverse_stmt)
  db.session.commit()

  update_request_query = db.update(t_friend_request)\
    .where(t_friend_request.c.friend_request_id == friend_request_id)\
    .values(accepted_at=func.now())
  db.session.execute(update_request_query)
  db.session.commit()

  return SUCCESS_ACCEPT_FRIEND_REQUEST.get_response()


@friend_bp.route("/ignore-request", methods=["POST"])
@jwt_required()
@check_jwt_user
@use_kwargs(RequestFriendIgnoreRequestSchema)
@marshal_with(ResponseError)
@doc(tags=[API_CATEGORY],
     summary="Ignore Friend Request",
     description="Ignores a friend request specified via friend request ID",
     params=authorization_header)
def friend_ignore_request(user, friend_request_id):
  friend_request = db.session.query(t_friend_request.c.user_id, t_friend_request.c.friend_id)\
    .filter(t_friend_request.c.friend_request_id == friend_request_id)\
    .scalar()
  if not friend_request:
    return ERROR_NONEXISTENT_FRIEND_REQUEST.get_response()

  update_request_query = db.update(t_friend_request)\
    .where(t_friend_request.c.friend_request_id == friend_request_id)\
    .values(ignored_at=func.now())
  db.session.execute(update_request_query)
  db.session.commit()

  return SUCCESS_IGNORE_FRIEND_REQUEST.get_response()
