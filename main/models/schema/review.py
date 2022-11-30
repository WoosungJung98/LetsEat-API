from marshmallow import Schema, fields, validate


# Requests
class RequestRestaurantReviewSchema(Schema):
  business_id = fields.Str(required = True,
                             validate = validate.Length(min = 3, max = 255))
  star = fields.Integer(required = False,
                          validate = validate.Range(min = 0, max = ))
  funny = fields.Integer(required = False,
                           validate = validate.Range(min = 0, max = 180))
  useful = fields.Integer(required = False,
                        validate = validate.Range(min = 0, max = 100000))
  cool = fields.Integer()

# Responses
