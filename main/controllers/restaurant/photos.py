from main import db
from main.controllers.restaurant import restaurant_bp, API_CATEGORY
from flask_apispec import marshal_with, doc
from main.controllers.common.common import (
    convert_query_to_response,
    escape_wildcards
)
from main.models.common.error import ResponseError
from main.models.restaurant.resources import ResponseRestaurantPhotoSchema
from main.models.photos import t_photos

@restaurant_bp.route("/<string:business_id>/photos", methods=["GET"])
@marshal_with(ResponseRestaurantPhotoSchema, code=200)
@marshal_with(ResponseError)
@doc(
    tags=[API_CATEGORY],
    summary="Restaurant Photos",
    description="Return photos for a given business"
)
def business_photos(business_id):
  print(business_id)  
  business_photos_query=db.select(t_photos.c.business_id, t_photos.c.photo_id, t_photos.c.caption, t_photos.c.label).filter(t_photos.c.business_id == business_id)
  result = db.session.execute(business_photos_query)

  business_photo_result={}
  business_photo_result["business_photo"] = [{
    "photo_id": photo.photo_id,
    "caption": photo.caption,
    "label": photo.label,
    } for photo in result]
  print('printing results')
  print(business_photo_result)
  return business_photo_result

