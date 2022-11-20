from flask_apispec import marshal_with, doc
from flask_jwt_extended import jwt_required

from main.controllers.user import user_bp, API_CATEGORY, authorization_header
from main.controllers.common.jwt import check_jwt_user
from main.models.common.error import ResponseError
from main.models.user import t_user
from main.models.schema.user import ResponseUserInfoSchema
from main import db


@user_bp.route("/info", methods=["GET"])
@jwt_required()
@check_jwt_user
@marshal_with(ResponseError)
@marshal_with(ResponseUserInfoSchema, code=200)
@doc(tags=[API_CATEGORY],
     summary="Get User Info",
     description="Returns the detailed information for the user",
     params=authorization_header)
def user_info(user):
  return {
      "user_name": user.user_name,
      "email": user.email,
      "profile_photo": user.profile_photo,
      "review_count": user.review_count,
      "useful": user.useful,
      "funny": user.funny,
      "cool": user.cool
  }
