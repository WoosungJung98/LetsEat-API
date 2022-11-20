from flask_apispec import use_kwargs, marshal_with, doc

from main.controllers.user import user_bp, API_CATEGORY
from main.controllers.common.common import (
    get_page_offset,
    check_pagination_request
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
  query = db.select(
    t_user.c.user_name,
    t_user.c.email,
    t_user.c.profile_photo,
    t_user.c.review_count,
    t_user.c.created_at)
  if user_name:
    query = query.where(func.lower(t_user.c.user_name).like(f"%{user_name.strip().lower()}%"))

  total_length = db.session.query(query.subquery()).count()

  if order_column == "user_name":
    order = t_user.c.user_name
  order = order.desc() if order_desc else order
  
  query = query.order_by(order)

  if length > 0:
    page_offset = get_page_offset(page, length)
    query = query.offset(page_offset)\
                 .limit(length)

  result = db.session.execute(query)
  return {
      "user": {
          "list": [{
            "user_name": user.user_name,
            "email": user.email,
            "profile_photo": user.profile_photo,
            "review_count": user.review_count,
            "created_at": user.created_at,
          } for user in result],
          "page": page,
          "total_length": total_length
      }
  }
