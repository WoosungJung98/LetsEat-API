from marshmallow import Schema, fields, validate


# Requests
class RequestLoginSchema(Schema):
  email = fields.Str(required=True)
  password = fields.Str(required=True,
                        validate = validate.Length(min = 8, max = 255))


class RequestChangePassword(Schema):
  old_password = fields.Str(required=True,
                            validate = validate.Length(min = 8, max = 255))
  new_password = fields.Str(required=True,
                            validate = validate.Length(min = 8, max = 255))


class RequestCreateAccountSchema(Schema):
  user_name = fields.Str(required=True,
                         validate = validate.Length(min = 3, max = 255))
  email = fields.Str(required=True,
                     validate = validate.Length(min = 3, max = 255))
  password = fields.Str(required=True,
                        validate = validate.Length(min = 8, max = 255))
  password_confirm = fields.Str(required=True,
                                validate = validate.Length(min = 8, max = 255))


class RequestVerifyEmailSchema(Schema):
  email = fields.Str(required=True,
                     validate = validate.Length(min = 3, max = 255))


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
