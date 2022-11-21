from flask import current_app as app
from flask_apispec import use_kwargs, marshal_with, doc

from main.controllers.user import (
    user_bp,
    API_CATEGORY,
    FACEYELP_API_CACHE
)
from main.controllers.common.common import (
    get_page_offset,
    check_pagination_request,
    convert_query_to_response
)
from main.models.common.error import ResponseError
from main.models.schema.user import (
    RequestUserListSchema,
    ResponseUserListSchema
)
from main.models.user import t_user
from main import db
from sqlalchemy import func


@user_bp.route("/list", methods=["GET"])
@use_kwargs(RequestUserListSchema, location="query")
@marshal_with(ResponseError)
@marshal_with(ResponseUserListSchema, code=200)
@doc(
    tags=[API_CATEGORY],
    summary="Get User List",
    description="Returns the list of users (searchable by name)"
)
@check_pagination_request
def user_list(page, length, user_name, order_column, order_desc):
  query = db.session.query(
    t_user.c.user_id,
    t_user.c.user_name,
    t_user.c.email,
    t_user.c.profile_photo,
    t_user.c.review_count,
    t_user.c.created_at)
  if user_name:
    query = query.filter(func.lower(t_user.c.user_name).like(f"%{user_name.strip().lower()}%"))
    cache_key = f"user_total_counts_{user_name.strip().lower()}"
  else:
    cache_key = "user_total_counts"
  
  if not FACEYELP_API_CACHE.exists(cache_key):
    FACEYELP_API_CACHE.setex(cache_key,
                             app.config["USER_TOTAL_LENGTH_CACHE_EXPIRE_TIME"],
                             query.count())
  total_length = FACEYELP_API_CACHE.get(cache_key)

  if order_column == "user_name":
    order = t_user.c.user_name
  order = order.desc() if order_desc else order
  
  query = query.order_by(order)

  if length > 0:
    page_offset = get_page_offset(page, length)
    query = query.offset(page_offset)\
                 .limit(length)

  result = query.all()
  attrs = ("user_id", "user_name", "email", "profile_photo", "review_count", "created_at")

  return {
      "user": {
          "list": convert_query_to_response(attrs, result),
          "page": page,
          "total_length": total_length
      }
  }
