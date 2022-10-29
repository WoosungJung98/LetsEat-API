from main import db
from main.controllers.restaurant import restaurant_bp, API_CATEGORY
from flask_apispec import marshal_with, doc
from main.controllers.common.common import (
    convert_query_to_response,
    escape_wildcards
)
from main.models.common.error import ResponseError
from main.models.restaurant.resources import ResponseRestaurantInfoSchema
from main.models.business import t_business

@restaurant_bp.route("/<string:business_id>/info", methods=["GET"])
@marshal_with(ResponseRestaurantInfoSchema, code=200)
@marshal_with(ResponseError)
@doc(
    tags=[API_CATEGORY],
    summary="Restaurant Info",
    description="Shows detailed info of Restaurant"
)
def restaurant_info(business_id):
  restaurant_info_query=db.select(t_business).filter(t_business.c.business_id == business_id)
  restaurant_info_result=db.session.execute(restaurant_info_query)
  restaurant= restaurant_info_result.fetchone()
  
  return {
    "business_info": {
      "business_id": restaurant.business_id,
      "business_name": restaurant.business_name,
      "address": restaurant.address,
      "city": restaurant.city,
      "state": restaurant.state,
      "postal_code": restaurant.postal_code,
      "latitude": restaurant.latitude,
      "longitude": restaurant.longitude,
      "stars": restaurant.stars,
      "review_count": restaurant.review_count,
      "is_open": restaurant.is_open,
      "categories": restaurant.categories,
      "hours": {
        "mon" : restaurant.hours.get('Monday', "Closed"),
        "tues" : restaurant.hours.get('Tuesday', "Closed"),
        "wed" : restaurant.hours.get('Wednesday', "Closed"),
        "thurs" : restaurant.hours.get('Thursday', "Closed"),
        "fri" : restaurant.hours.get('Friday', "Closed"),
        "sat" : restaurant.hours.get('Saturday', "Closed"),
        "sun" : restaurant.hours.get('Sunday', "Closed")
      }
    }
  }
