from flask_apispec import marshal_with, doc
from flask_jwt_extended import jwt_required

from main.controllers.meal import meal_bp, API_CATEGORY, authorization_header
from main.controllers.common.jwt import check_jwt_user
from main.models.common.error import ResponseError
from main.models.schema.meal import ResponseMealListSchema
from main.models.user import t_user
from main.models.meal import t_meal
from main.models.business import t_business
from main import db
from sqlalchemy import func


@meal_bp.route("/list", methods=["GET"])
@jwt_required()
@check_jwt_user
@marshal_with(ResponseError)
@marshal_with(ResponseMealListSchema, code=200)
@doc(tags=[API_CATEGORY],
     summary="Get Meal List",
     description="Returns the list of upcoming meals for the user",
     params=authorization_header)
def meal_list(user):
  query = db\
    .select(
      t_meal.c.meal_id.label("meal_id"),
      t_user.c.user_name.label("friend_name"),
      t_user.c.avatar_num.label("avatar_num"),
      t_business.c.business_name.label("restaurant_name"),
      t_business.c.address.label("restaurant_address"),
      t_meal.c.meal_at.label("meal_at")
    )\
    .join(t_user, t_meal.c.friend_id == t_user.c.user_id)\
    .join(t_business, t_meal.c.restaurant_id == t_business.c.business_id)\
    .where(t_meal.c.user_id == user.user_id)\
    .where(t_meal.c.meal_at > func.now())\
    .order_by(t_meal.c.meal_at)
  result = db.session.execute(query)

  meal_results={}
  meal_results["meal_list"] = [{
    "meal_id": meal.meal_id,
    "friend_name": meal.friend_name,
    "avatar_num": meal.avatar_num,
    "restaurant_name": meal.restaurant_name,
    "restaurant_address": meal.restaurant_address,
    "meal_at": meal.meal_at
  } for meal in result]

  return meal_results
