from flask_apispec import use_kwargs, marshal_with, doc
from flask_jwt_extended import jwt_required

from main.controllers.meal import meal_bp, API_CATEGORY, authorization_header
from main.controllers.common.jwt import check_jwt_user
from main.models.common.error import (
    ResponseError,
    ERROR_NONEXISTENT_FRIEND,
    ERROR_NONEXISTENT_RESTAURANT,
    ERROR_FRIEND_REQUIRED_MEAL_REQUEST,
    ERROR_INVALID_MEAL_TIME,
    ERROR_MEAL_ALREADY_SCHEDULED,
    ERROR_MEAL_REQUEST_ALREADY_SENT,
    SUCCESS_SEND_MEAL_REQUEST,
    ERROR_NONEXISTENT_MEAL_REQUEST,
    ERROR_MEAL_REQUEST_UNAUTHORIZED,
    SUCCESS_ACCEPT_MEAL_REQUEST,
    SUCCESS_IGNORE_MEAL_REQUEST
)
from main.models.schema.meal import (
    RequestMealSendRequestSchema,
    RequestMealAcceptRequestSchema,
    RequestMealIgnoreRequestSchema,
    ResponseMealRequestListSchema
)
from main.models.meal import t_meal
from main.models.meal_request import t_meal_request
from main.models.user import t_user, get_user
from main.models.friend import t_friend
from main.models.business import t_business
from main import db
from sqlalchemy import extract, func
from sqlalchemy.dialects.postgresql import insert
from datetime import datetime, timezone

MEAL_REQUEST_LIST_LENGTH = 10


@meal_bp.route("/requests", methods=["GET"])
@jwt_required()
@check_jwt_user
@marshal_with(ResponseError)
@marshal_with(ResponseMealRequestListSchema, code=200)
@doc(tags=[API_CATEGORY],
     summary="Get Meal Request List",
     description="Returns the list of actionable meal requests for given user",
     params=authorization_header)
def meal_requests(user):
  query = db\
    .select(
      t_meal_request.c.meal_request_id,
      t_user.c.user_name,
      t_user.c.avatar_num,
      t_business.c.business_name.label("restaurant_name"),
      t_business.c.address.label("restaurant_address"),
      t_meal_request.c.meal_at,
      t_meal_request.c.created_at)\
    .join(t_user, t_meal_request.c.user_id == t_user.c.user_id)\
    .join(t_business, t_meal_request.c.restaurant_id == t_business.c.business_id)\
    .where(t_meal_request.c.friend_id == user.user_id)\
    .where(t_meal_request.c.accepted_at == None)\
    .where(t_meal_request.c.ignored_at == None)\
    .order_by(t_meal_request.c.created_at.desc())\
    .limit(MEAL_REQUEST_LIST_LENGTH)
  
  result = db.session.execute(query)
  meal_request_results={}
  meal_request_results["meal_request_list"] = [{
    "meal_request_id": meal_request.meal_request_id,
    "user_name": meal_request.user_name,
    "avatar_num": meal_request.avatar_num,
    "restaurant_name": meal_request.restaurant_name,
    "restaurant_address": meal_request.restaurant_address,
    "meal_at": meal_request.meal_at,
    "created_at": meal_request.created_at,
  } for meal_request in result]

  return meal_request_results


@meal_bp.route("/send-request", methods=["POST"])
@jwt_required()
@check_jwt_user
@use_kwargs(RequestMealSendRequestSchema)
@marshal_with(ResponseError)
@doc(tags=[API_CATEGORY],
     summary="Send Meal Request",
     description="Sends meal request to target user",
     params=authorization_header)
def meal_send_request(user, friend_id, restaurant_id, meal_at):
  if not get_user(friend_id):
    return ERROR_NONEXISTENT_FRIEND.get_response()

  friend_query = db.session.query(t_friend.c.user_id)\
                   .filter(t_friend.c.user_id == user.user_id)\
                   .filter(t_friend.c.friend_id == friend_id)
  reverse_query = db.session.query(t_friend.c.user_id)\
                    .filter(t_friend.c.user_id == friend_id)\
                    .filter(t_friend.c.friend_id == user.user_id)
  result = friend_query.union_all(reverse_query).count()
  if result != 2:
    return ERROR_FRIEND_REQUIRED_MEAL_REQUEST.get_response()
  
  restaurant_query = db.session.query(t_business.c.business_id).filter(t_business.c.business_id == restaurant_id)
  if not db.session.query(restaurant_query.exists()).scalar():
    return ERROR_NONEXISTENT_RESTAURANT.get_response()
  if meal_at < datetime.now(timezone.utc):
    return ERROR_INVALID_MEAL_TIME.get_response()

  meal_query = db.session.query(t_meal.c.meal_id)\
    .filter(t_meal.c.user_id == user.user_id)\
    .filter(t_meal.c.friend_id == friend_id)\
    .filter(t_meal.c.restaurant_id == restaurant_id)\
    .filter(t_meal.c.meal_at == meal_at)
  if db.session.query(meal_query.exists()).scalar():
    return ERROR_MEAL_ALREADY_SCHEDULED.get_response()

  try:
    add_meal_request_query = db.insert(t_meal_request)\
      .values(
        user_id=user.user_id,
        friend_id=friend_id,
        restaurant_id=restaurant_id,
        meal_at=meal_at,
        created_at=func.now())
    db.session.execute(add_meal_request_query)
    db.session.commit()
  except:
    return ERROR_MEAL_REQUEST_ALREADY_SENT.get_response()

  return SUCCESS_SEND_MEAL_REQUEST.get_response()


@meal_bp.route("/accept-request", methods=["POST"])
@jwt_required()
@check_jwt_user
@use_kwargs(RequestMealAcceptRequestSchema)
@marshal_with(ResponseError)
@doc(tags=[API_CATEGORY],
     summary="Accept Meal Request",
     description="Accepts a meal request specified via meal request ID",
     params=authorization_header)
def meal_accept_request(user, meal_request_id):
  meal_request = db.session.execute(
    db.select(
      t_meal_request.c.user_id,
      t_meal_request.c.friend_id,
      t_meal_request.c.restaurant_id,
      t_meal_request.c.meal_at)\
    .where(t_meal_request.c.meal_request_id == meal_request_id)\
    .where(t_meal_request.c.accepted_at == None)\
    .where(t_meal_request.c.ignored_at == None))\
    .fetchone()
  if not meal_request:
    return ERROR_NONEXISTENT_MEAL_REQUEST.get_response()
  if meal_request.friend_id != user.user_id:
    return ERROR_MEAL_REQUEST_UNAUTHORIZED.get_response()

  insert_stmt = insert(t_meal).values({
    t_meal.c.user_id: meal_request.user_id,
    t_meal.c.friend_id: meal_request.friend_id,
    t_meal.c.restaurant_id: meal_request.restaurant_id,
    t_meal.c.meal_at: meal_request.meal_at,
    t_meal.c.created_at: func.now()
  })
  do_nothing_stmt = insert_stmt.on_conflict_do_nothing(
    index_elements=[t_meal.c.user_id, t_meal.c.friend_id, t_meal.c.restaurant_id, t_meal.c.meal_at]
  )
  db.session.execute(do_nothing_stmt)
  db.session.commit()

  insert_reverse_stmt = insert(t_meal).values({
    t_meal.c.user_id: meal_request.friend_id,
    t_meal.c.friend_id: meal_request.user_id,
    t_meal.c.restaurant_id: meal_request.restaurant_id,
    t_meal.c.meal_at: meal_request.meal_at,
    t_meal.c.created_at: func.now()
  })
  do_nothing_reverse_stmt = insert_reverse_stmt.on_conflict_do_nothing(
    index_elements=[t_meal.c.user_id, t_meal.c.friend_id, t_meal.c.restaurant_id, t_meal.c.meal_at]
  )
  db.session.execute(do_nothing_reverse_stmt)
  db.session.commit()

  update_request_query = db.update(t_meal_request)\
    .where(t_meal_request.c.meal_request_id == meal_request_id)\
    .values(accepted_at=func.now())
  db.session.execute(update_request_query)
  db.session.commit()

  return SUCCESS_ACCEPT_MEAL_REQUEST.get_response()


@meal_bp.route("/ignore-request", methods=["POST"])
@jwt_required()
@check_jwt_user
@use_kwargs(RequestMealIgnoreRequestSchema)
@marshal_with(ResponseError)
@doc(tags=[API_CATEGORY],
     summary="Ignore Meal Request",
     description="Ignores a meal request specified via meal request ID",
     params=authorization_header)
def meal_ignore_request(user, meal_request_id):
  meal_request = db.session.execute(
    db.select(t_meal_request.c.friend_id)\
    .where(t_meal_request.c.meal_request_id == meal_request_id)\
    .where(t_meal_request.c.accepted_at == None)\
    .where(t_meal_request.c.ignored_at == None))\
    .fetchone()
  if not meal_request:
    return ERROR_NONEXISTENT_MEAL_REQUEST.get_response()
  if meal_request.friend_id != user.user_id:
    return ERROR_MEAL_REQUEST_UNAUTHORIZED.get_response()

  update_request_query = db.update(t_meal_request)\
    .where(t_meal_request.c.meal_request_id == meal_request_id)\
    .values(ignored_at=func.now())
  db.session.execute(update_request_query)
  db.session.commit()

  return SUCCESS_IGNORE_MEAL_REQUEST.get_response()
