from marshmallow import Schema, fields, validate


# Requests
class RequestRestaurantListSchema(Schema):
  business_name = fields.Str(required = True,
                            validate = validate.Length(min = 3, max = 255))
  latitude = fields.Float(required = True,
                          validate = validate.Range(min = -90, max = 90))
  longitude = fields.Float(required = True,
                           validate = validate.Range(min = -180, max = 180))
  radius = fields.Float(required = False,
                        validate = validate.Range(min = 1))
  length = fields.Integer(required = False,
                        validate = validate.Range(min = 1, max = 100))


# Responses
class BusinessList(Schema):
  business_id = fields.Str(data_key="businessID")
  business_name = fields.Str(data_key="businessName")
  address = fields.Str()
  city = fields.Str()
  longitude = fields.Float()
  latitude = fields.Float()


class ResponseRestaurantListSchema(Schema):
  business_list = fields.List(fields.Nested(BusinessList), data_key="businessList")


class BusinessHour(Schema):
  mon = fields.Str()
  tues = fields.Str()
  wed = fields.Str()
  thurs  = fields.Str()
  fri= fields.Str()
  sat = fields.Str()
  sun = fields.Str()


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
  hours = fields.Nested(BusinessHour)


class ResponseRestaurantInfoSchema(Schema):
  business_info = fields.Nested(BusinessInfo, data_key="businessInfo")
