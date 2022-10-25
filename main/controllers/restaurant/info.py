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
  return {
    "business_info": {
      "business_id": "sd_f2as34da",
      "business_name": "Chipotle",
      "address": "123 Elm St",
      "city": "New Haven",
      "state": "CT",
      "postal_code": "06511",
      "latitude": 123.34,
      "longitude": 342.12,
      "stars": 4.2,
      "review_count": 1234,
      "is_open": True,
      "attributes": {
        "is_good": True,
        "is_tasty": True,
        "max_people": 35
      },
      "categories": [
        "mexican",
        "fusion"
      ],
      "hours": {
        "Monday": "12:00-21:00",
        "Tuesday": "12:00-21:00"
      }
    }
  }
