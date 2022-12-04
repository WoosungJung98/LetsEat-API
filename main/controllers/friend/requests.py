from flask_apispec import use_kwargs, marshal_with, doc
from flask_jwt_extended import jwt_required

from main.controllers.friend import friend_bp, API_CATEGORY, authorization_header
from main.controllers.common.jwt import check_jwt_user
from main.models.common.error import (
    ResponseError,
    ERROR_NONEXISTENT_FRIEND,
    ERROR_NO_SELF_FRIEND_REQUEST,
    ERROR_NONEXISTENT_FRIEND_REQUEST,
    ERROR_ALREADY_FRIENDS,
    ERROR_FRIEND_REQUEST_UNAUTHORIZED,
    ERROR_FRIEND_REQUEST_ALREADY_SENT,
    SUCCESS_SEND_FRIEND_REQUEST,
    SUCCESS_ACCEPT_FRIEND_REQUEST,
    SUCCESS_IGNORE_FRIEND_REQUEST
)
from main.models.schema.friend import (
    RequestFriendSendRequestSchema,
    RequestFriendAcceptRequestSchema,
    RequestFriendIgnoreRequestSchema,
    ResponseFriendRequestListSchema
)
from main.models.friend_request import t_friend_request
from main.models.user import t_user, get_user
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
      t_user.c.avatar_num,
      t_friend_request.c.created_at)\
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
    "avatar_num": friend_request.avatar_num,
    "created_at": friend_request.created_at,
  } for friend_request in result]

  return friend_request_results


@friend_bp.route("/send-request", methods=["POST"])
@jwt_required()
@check_jwt_user
@use_kwargs(RequestFriendSendRequestSchema)
@marshal_with(ResponseError)
@doc(tags=[API_CATEGORY],
     summary="Send Friend Request",
     description="Sends friend request to target user",
     params=authorization_header)
def friend_send_request(user, friend_id):
  if user.user_id == friend_id:
    return ERROR_NO_SELF_FRIEND_REQUEST.get_response()
  if not get_user(friend_id):
    return ERROR_NONEXISTENT_FRIEND.get_response()
  
  friend_query = db.session.query(t_friend.c.user_id)\
                   .filter(t_friend.c.user_id == user.user_id)\
                   .filter(t_friend.c.friend_id == friend_id)
  reverse_query = db.session.query(t_friend.c.user_id)\
                    .filter(t_friend.c.user_id == friend_id)\
                    .filter(t_friend.c.friend_id == user.user_id)
  result = friend_query.union_all(reverse_query).count()
  if result == 2:
    return ERROR_ALREADY_FRIENDS.get_response()

  try:
    add_friend_request_query = db.insert(t_friend_request)\
      .values(user_id=user.user_id, friend_id=friend_id, created_at=func.now())
    db.session.execute(add_friend_request_query)
    db.session.commit()
  except:
    return ERROR_FRIEND_REQUEST_ALREADY_SENT.get_response()

  return SUCCESS_SEND_FRIEND_REQUEST.get_response()


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
  friend_request = db.session.execute(
    db.select(t_friend_request.c.user_id, t_friend_request.c.friend_id)\
    .where(t_friend_request.c.friend_request_id == friend_request_id)\
    .where(t_friend_request.c.accepted_at == None)\
    .where(t_friend_request.c.ignored_at == None))\
    .fetchone()
  if not friend_request:
    return ERROR_NONEXISTENT_FRIEND_REQUEST.get_response()
  if friend_request.friend_id != user.user_id:
    return ERROR_FRIEND_REQUEST_UNAUTHORIZED.get_response()

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
  friend_request = db.session.execute(
    db.select(t_friend_request.c.friend_id)\
    .where(t_friend_request.c.friend_request_id == friend_request_id)\
    .where(t_friend_request.c.accepted_at == None)\
    .where(t_friend_request.c.ignored_at == None))\
    .fetchone()
  if not friend_request:
    return ERROR_NONEXISTENT_FRIEND_REQUEST.get_response()
  if friend_request.friend_id != user.user_id:
    return ERROR_FRIEND_REQUEST_UNAUTHORIZED.get_response()

  update_request_query = db.update(t_friend_request)\
    .where(t_friend_request.c.friend_request_id == friend_request_id)\
    .values(ignored_at=func.now())
  db.session.execute(update_request_query)
  db.session.commit()

  return SUCCESS_IGNORE_FRIEND_REQUEST.get_response()
