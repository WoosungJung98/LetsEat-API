from main import db
from main.controllers.restaurant import restaurant_bp, API_CATEGORY
from flask_apispec import marshal_with, doc
from main.models.common.error import (
    ResponseError,
    ERROR_BUSINESS_ID_NOT_EXISTS_PATH
)
from main.models.schema.review import ResponseRestaurantReviewSchema
from main.models.business import get_restaurant

@restaurant_bp.route("/<string:business_id>/reviews", methods=["GET"])
@marshal_with(ResponseRestaurantReviewSchema, code=200)
@marshal_with(ResponseError)
@doc(
    tags=[API_CATEGORY],
    summary="Restaurant Reviews",
    description="Shows the reviews of a restaurant"
)
def restaurant_reviews(business_id):
  restaurant = get_restaurant(business_id)
  if not restaurant:
    return ERROR_BUSINESS_ID_NOT_EXISTS_PATH.get_response()
  return {
    "business_info": {
      
  }
