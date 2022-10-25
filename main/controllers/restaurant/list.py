from main import db
from main.controllers.restaurant import restaurant_bp, API_CATEGORY
from flask_apispec import use_kwargs, marshal_with, doc
from main.controllers.common.common import (
    convert_query_to_response,
    escape_wildcards
)
from main.models.common.error import ResponseError
from main.models.restaurant.resources import (
    RequestRestaurantListSchema,
    ResponseRestaurantListSchema
)
from main.models.business import t_business


@restaurant_bp.route("/list", methods=["GET"])
@use_kwargs(RequestRestaurantListSchema, location="query")
@marshal_with(ResponseRestaurantListSchema, code=200)
@marshal_with(ResponseError)
@doc(
    tags=[API_CATEGORY],
    summary="Restaurant List",
    description="Shows list of Restaurants"
)
def restaurant_list(business_name, latitude, longitude):
  return {
    "business_list": [
      {
        "business_id": "sd_f2as34da",
        "business_name": "Chipotle",
        "address": "123 Elm St",
        "city": "New Haven"
      }
    ]
  }
