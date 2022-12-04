from marshmallow import Schema, fields, validate


# Requests
class RequestMealSendRequestSchema(Schema):
  friend_id = fields.Str(required=True,
                         validate = validate.Length(equal = 22))
  restaurant_id = fields.Str(required=True,
                             validate = validate.Length(equal = 22))
  meal_at = fields.DateTime(format="iso", required=True)
                            

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
  restaurant_address = fields.Str(data_key="restaurantAddress")
  meal_at = fields.DateTime(format="iso", data_key="mealAt")


class MealRequest(Schema):
  meal_request_id = fields.Str(data_key="mealRequestID")
  user_name = fields.Str(data_key="userName")
  avatar_num = fields.Int(data_key="avatarNum")
  created_at = fields.DateTime(format="iso", data_key="createdAt")
  restaurant_name = fields.Str(data_key="restaurantName")
  restaurant_address = fields.Str(data_key="restaurantAddress")
  meal_at = fields.DateTime(format="iso", data_key="mealAt")


class ResponseMealListSchema(Schema):
  meal_list = fields.List(fields.Nested(MealList), data_key="mealList")


class ResponseMealRequestListSchema(Schema):
  meal_request_list = fields.List(fields.Nested(MealRequest), data_key="mealRequestList")
