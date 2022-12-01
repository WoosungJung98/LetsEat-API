from marshmallow import Schema, fields, validate
from main.models.common.common import DateTime


# Requests
class RequestMealSendRequestSchema(Schema):
  friend_id = fields.Str(required=True,
                         validate = validate.Length(equal = 22))
  restaurant_id = fields.Str(required=True,
                             validate = validate.Length(equal = 22))
  meal_at = DateTime(required=True)


class RequestMealAcceptRequestSchema(Schema):
  meal_request_id = fields.Int(required=True)


class RequestMealIgnoreRequestSchema(Schema):
  meal_request_id = fields.Int(required=True)


# Responses
class MealList(Schema):
  friend_name = fields.Str(data_key="friendName")
  avatar_num = fields.Int(data_key="avatarNum")
  restaurant_name = fields.Str(data_key="restaurantName")
  meal_at = DateTime(data_key="mealAt")


class MealRequest(Schema):
  meal_request_id = fields.Str(data_key="mealRequestID")
  user_name = fields.Str(data_key="userName")
  avatar_num = fields.Int(data_key="avatarNum")
  time_diff = fields.Int(data_key="timeDiff")


class ResponseMealListSchema(Schema):
  meal_list = fields.List(fields.Nested(MealList), data_key="mealList")


class ResponseMealRequestListSchema(Schema):
  meal_request_list = fields.List(fields.Nested(MealRequest), data_key="mealRequestList")
