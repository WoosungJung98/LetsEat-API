from marshmallow import Schema, fields, validate


# Requests
class RequestRestaurantListSchema(Schema):
  business_name = fields.Str(required=True,
                             validate=validate.Length(min=3, max=255))
  latitude = fields.Float(required=True,
                          validate=validate.Range(min=-90, max=90))
  longitude = fields.Float(required=True,
                           validate=validate.Range(min=-180, max=180))


# Responses
class BusinessList(Schema):
  business_id = fields.Str(data_key="businessID")
  business_name = fields.Str(data_key="businessName")
  address = fields.Str()
  city = fields.Str()


class ResponseRestaurantListSchema(Schema):
  business_list = fields.List(fields.Nested(BusinessList), data_key="businessList")


class BusinessInfo(Schema):
  business_id = fields.Str(data_key="businessID")
  business_name = fields.Str(data_key="businessName")
  address = fields.Str()
  city = fields.Str()
  state = fields.Str()
  postal_code = fields.Str(data_key="postalCode")
  latitude = fields.Float()
  longitude = fields.Float()
  stars = fields.Float()
  review_count = fields.Integer(data_key="reviewCount")
  is_open = fields.Bool(data_key="isOpen")
  attributes = fields.Dict()
  categories = fields.List(fields.Str())
  hours = fields.Dict()


class ResponseRestaurantInfoSchema(Schema):
  business_info = fields.Nested(BusinessInfo, data_key="businessInfo")
