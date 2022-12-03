from marshmallow import Schema, fields, validate
from main.controllers.common.date import DATETIME_PATTERN


# Requests
class RequestMealSendRequestSchema(Schema):
  friend_id = fields.Str(required=True,
                         validate = validate.Length(equal = 22))
  restaurant_id = fields.Str(required=True,
                             validate = validate.Length(equal = 22))
  meal_at = fields.DateTime(format=DATETIME_PATTERN, required=True)
                            

class RequestMealAcceptRequestSchema(Schema):
  meal_request_id = fields.Int(required=True)


class RequestMealIgnoreRequestSchema(Schema):
  meal_request_id = fields.Int(required=True)


# Responses
class MealList(Schema):
  id = fields.Int()
  friend_name = fields.Str(data_key="friendName")
  avatar_num = fields.Int(data_key="avatarNum")
  restaurant_name = fields.Str(data_key="restaurantName")
  address = fields.Str()
  meal_at = fields.DateTime(format=DATETIME_PATTERN, data_key="mealAt")


class MealRequest(Schema):
  meal_request_id = fields.Str(data_key="mealRequestID")
  user_name = fields.Str(data_key="userName")
  avatar_num = fields.Int(data_key="avatarNum")
  time_diff = fields.Int(data_key="timeDiff")
  restaurant_name = fields.Str(data_key="restaurantName")
  meal_at = fields.DateTime(format=DATETIME_PATTERN, data_key="mealAt")


class ResponseMealListSchema(Schema):
  meal_list = fields.List(fields.Nested(MealList), data_key="mealList")


class ResponseMealRequestListSchema(Schema):
  meal_request_list = fields.List(fields.Nested(MealRequest), data_key="mealRequestList")
