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
from main.models.common.error import (
    ResponseError,
    ERROR_BUSINESS_ID_NOT_EXISTS_PATH
)
from main.models.schema.user import (
    RequestRestaurantReviewSchema,
    ReviewList
)
from main.models.business import get_restaurant
from main.models.user import t_user, t_user_name_cnt_map
from main import db
#from sqlalchemy import func, and_


@user_bp.route("/reviews", methods=["GET"])
@jwt_required()
@check_jwt_user
@use_kwargs(RequestRestaurantReviewSchema, location="query")
@marshal_with(ResponseError)
@marshal_with(ReviewList, code=200)
@doc(
    tags=[API_CATEGORY],
    summary="Get Restaurant Reviews",
    description="Returns the list of reviews for a restaurant",
    params=authorization_header
)
@check_pagination_request
def review_list(user, page, length, business_id, star, funny, useful, cool):
    restaurant = get_restaurant(business_id)
    if not restaurant:
        return ERROR_BUSINESS_ID_NOT_EXISTS_PATH.get_response()
    query = db.session.query( t_review

  return {
      []
  }
