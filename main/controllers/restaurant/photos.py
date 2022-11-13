from main import db
from main.controllers.restaurant import restaurant_bp, API_CATEGORY
from flask_apispec import marshal_with, doc
from main.models.common.error import (
    ResponseError,
    ERROR_BUSINESS_ID_NOT_EXISTS_PATH
)
from main.models.schema.restaurant import ResponseRestaurantPhotoSchema
from main.models.photo import t_photo
from main.models.business import get_restaurant

@restaurant_bp.route("/<string:business_id>/photos", methods=["GET"])
@marshal_with(ResponseRestaurantPhotoSchema, code=200)
@marshal_with(ResponseError)
@doc(
    tags=[API_CATEGORY],
    summary="Restaurant Photos",
    description="Return photos for a given business"
)
def restaurant_photos(business_id):
  restaurant = get_restaurant(business_id)
  if not restaurant:
    return ERROR_BUSINESS_ID_NOT_EXISTS_PATH.get_response()
  business_photos_query = db.select(
      t_photo.c.photo_id,
      t_photo.c.caption,
      t_photo.c.label)\
    .where(t_photo.c.business_id == business_id)
  result = db.session.execute(business_photos_query)

  business_photo_result = {}
  business_photo_result["business_photo_list"] = [{
    "photo_id": photo.photo_id,
    "caption": photo.caption,
    "label": photo.label,
  } for photo in result]
  return business_photo_result
