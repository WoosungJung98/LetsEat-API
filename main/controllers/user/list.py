from flask import current_app as app
from flask_apispec import use_kwargs, marshal_with, doc
from flask_jwt_extended import jwt_required

from main.controllers.user import (
    user_bp,
    API_CATEGORY,
    authorization_header
)
from main.controllers.common.common import (
    get_page_offset,
    check_pagination_request,
    convert_query_to_response
)
from main.controllers.common.jwt import check_jwt_user
from main.models.common.error import ResponseError
from main.models.schema.user import (
    RequestUserListSchema,
    ResponseUserListSchema
)
from main.models.user import t_user, t_user_name_cnt_map
from main.models.friend import t_friend
from main.models.friend_request import t_friend_request
from main import db
from sqlalchemy import func, and_


@user_bp.route("/list", methods=["GET"])
@jwt_required()
@check_jwt_user
@use_kwargs(RequestUserListSchema, location="query")
@marshal_with(ResponseError)
@marshal_with(ResponseUserListSchema, code=200)
@doc(
    tags=[API_CATEGORY],
    summary="Get User List",
    description="Returns the list of users (searchable by name)",
    params=authorization_header
)
@check_pagination_request
def user_list(user, page, length, user_name):
  query = db.session.query(
    t_user.c.user_id,
    t_user.c.user_name,
    t_user.c.email,
    t_user.c.profile_photo,
    t_user.c.avatar_num,
    t_user.c.review_count,
    t_user.c.created_at)
  total_length_query = db.session\
    .query(func.sum(t_user_name_cnt_map.c.cnt))
  if user_name:
    query = query.filter(func.lower(t_user.c.user_name).like(f"%{user_name.strip().lower()}%"))
    total_length_query = total_length_query\
      .filter(func.lower(t_user_name_cnt_map.c.user_name).like(f"%{user_name.strip().lower()}%"))
  
  query = query.order_by(t_user.c.user_id)

  if length > 0:
    page_offset = get_page_offset(page, length)
    query = query.offset(page_offset)\
                 .limit(length)

  subq = query.subquery()
  query = db.session\
    .query(
      subq,
      (t_friend.c.user_id != None).label("is_friend"),
      (t_friend_request.c.friend_request_id != None).label("has_sent_request"))\
    .outerjoin(
      t_friend,
      and_(
        t_friend.c.user_id == user.user_id,
        subq.c.user_id == t_friend.c.friend_id
      )
    )\
    .outerjoin(
      t_friend_request,
      and_(
        t_friend_request.c.user_id == user.user_id,
        t_friend_request.c.accepted_at == None,
        t_friend_request.c.ignored_at == None,
        subq.c.user_id == t_friend_request.c.friend_id
      )
    )

  result = query.all()
  attrs = ("user_id", "user_name", "email", "profile_photo", "avatar_num",
           "review_count", "created_at", "is_friend", "has_sent_request")
  return {
      "user": {
          "list": convert_query_to_response(attrs, result),
          "page": page,
          "total_length": total_length_query.scalar()
      }
  }
