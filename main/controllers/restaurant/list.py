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
from sqlalchemy import func

@restaurant_bp.route("/list", methods=["GET"])
@use_kwargs(RequestRestaurantListSchema, location="query")
@marshal_with(ResponseRestaurantListSchema, code=200)
@marshal_with(ResponseError)
@doc(
    tags=[API_CATEGORY],
    summary="Restaurant List",
    description="Shows list of Restaurants"
)
def restaurant_list(business_name, latitude, longitude, radius, length):
  business_name = escape_wildcards(business_name, ("%", "_"))
  query = db.select(t_business.c.business_id, t_business.c.business_name, t_business.c.address, t_business.c.city, t_business.c.latitude, t_business.c.longitude)\
            .where(func.earth_distance(func.ll_to_earth(latitude, longitude),
                                       func.ll_to_earth(t_business.c.latitude, t_business.c.longitude)) < radius)\
            .where(func.earth_box(func.ll_to_earth(latitude, longitude), radius).op("@>")(func.ll_to_earth(t_business.c.latitude, t_business.c.longitude)))\
            .where(func.lower(t_business.c.business_name).like(f"%{business_name.lower()}%"))\
            .order_by(func.earth_distance(func.ll_to_earth(latitude,longitude), 
                                          func.ll_to_earth(t_business.c.latitude, t_business.c.longitude)))\
            .limit(length)
  result = db.session.execute(query)
  business_results={}
  business_results["business_list"] = [{"business_id": business.business_id, 
                                        "business_name": business.business_name, 
                                        "address": business.address, 
                                        "city": business.address,
                                        "latitude": business.latitude,
                                        "longitude": business.longitude} for business in result]
    
  return business_results