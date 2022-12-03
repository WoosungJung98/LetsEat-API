from marshmallow import Schema, fields, validate


# Requests
class RequestRestaurantReviewSchema(RequestPagination):
  business_id = fields.Str(required = True,
                             validate = validate.Length(equal = 22))
  star = fields.Integer(required = False,
                          validate = validate.Range(min = 0, max = 5))
  funny = fields.Integer(required = False,
                           validate = validate.Range(min = 0, max = 100000000))
  useful = fields.Integer(required = False,
                        validate = validate.Range(min = 0, max = 100000000))
  cool = fields.Integer(required = False, 
                        validate = validate.Range(min = 0 , max = 100000000))

# Responses

class ReviewList(Schema):
  user_name = fields.Str(data_key="userName")
  stars = fields.Int()
  date = fields.Str()
  text = fields.Str()
  useful = fields.Int()
  funny = fields.Int()
  cool = fields.Int()