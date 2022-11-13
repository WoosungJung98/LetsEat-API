from marshmallow import Schema, fields


# Requests
class RequestLoginSchema(Schema):
  email = fields.Str(required=True)
  password = fields.Str(required=True)


class RequestChangePassword(Schema):
  old_password = fields.Str(required=True)
  new_password = fields.Str(required=True)


# Responses
class ResponseAccessTokenSchema(Schema):
  access_token = fields.Str(data_key="accessToken")


class ResponseLoginSchema(ResponseAccessTokenSchema):
  refresh_token = fields.Str(data_key="refreshToken")


class ResponseUserInfo(Schema):
  user_name = fields.Str(data_key="userName")
  email = fields.Str()
  profile_photo = fields.Str(data_key="profilePhoto")
  review_count = fields.Str(data_key="reviewCount")
  useful = fields.Int()
  funny = fields.Int()
  cool = fields.Int()
