from marshmallow import Schema, fields, validate
from main.models.common.common import (
    create_pagination_list_schema,
    DateTime,
    RequestPagination
)


# Requests
class RequestLoginSchema(Schema):
  email = fields.Str(required=True,
                     validate = validate.Length(min = 3, max = 255))
  password = fields.Str(required=True,
                        validate = validate.Length(min = 8, max = 255))


class RequestChangePasswordSchema(Schema):
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
  avatar_num = fields.Integer(required=True,
                              validate = validate.Range(min = 1, max = 24))


class RequestVerifyEmailSchema(Schema):
  email = fields.Str(required=True,
                     validate = validate.Length(min = 3, max = 255))


class RequestUserListSchema(RequestPagination):
  user_name = fields.Str(missing=None,
                         validate = validate.Length(min = 3, max = 255))


# Responses
class ResponseAccessTokenSchema(Schema):
  access_token = fields.Str(data_key="accessToken")


class ResponseLoginSchema(ResponseAccessTokenSchema):
  refresh_token = fields.Str(data_key="refreshToken")


class UserInfo(Schema):
  user_id = fields.Str(data_key="userID")
  user_name = fields.Str(data_key="userName")
  email = fields.Str()
  profile_photo = fields.Str(data_key="profilePhoto")
  avatar_num = fields.Int(data_key="avatarNum")
  review_count = fields.Str(data_key="reviewCount")
  useful = fields.Int()
  funny = fields.Int()
  cool = fields.Int()


class ResponseUserInfoSchema(Schema):
  user_info = fields.Nested(UserInfo, data_key="userInfo")


class UserListItem(Schema):
  user_id = fields.Str(data_key="userID", required=True)
  user_name = fields.Str(data_key="userName", required=True)
  email = fields.Str(required=True)
  profile_photo = fields.Str(data_key="profilePhoto", required=True, allow_none=True)
  avatar_num = fields.Int(data_key="avatarNum", required=True, allow_none=True)
  review_count = fields.Int(data_key="reviewCount", required=True)
  created_at = DateTime(data_key="createdAt", required=True)


class ResponseUserListSchema(Schema):
  user = fields.Nested(
      create_pagination_list_schema(UserListItem),
      required=True
  )
