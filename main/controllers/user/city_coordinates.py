from main import db
from main.controllers.user import user_bp, API_CATEGORY
from flask_apispec import marshal_with, doc
from main.controllers.common.common import convert_query_to_response
from main.models.common.error import ResponseError
from main.models.city import t_city
from main.models.schema.user import ResponseCityCoordinatesSchema
from sqlalchemy import func

@user_bp.route("/city-coordinates", methods=["GET"])
@marshal_with(ResponseCityCoordinatesSchema, code=200)
@marshal_with(ResponseError)
@doc(
    tags=[API_CATEGORY],
    summary="City Coordinates",
    description="Returns city coordinates"
)
def user_city_coordinates():
    query = db.session.query(func.concat(func.trim(t_city.c.city_name), ", ", t_city.c.postal_code), t_city.c.latitude, t_city.c.longitude )
    result = query.all()
    attrs = ("city_name", "latitude", "longitude")
    return {
        "city_coordinate_list": convert_query_to_response(attrs, result)
    }
