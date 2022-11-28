from marshmallow import Schema, fields, validate


# Requests
class RequestFriendListSchema(Schema):
  friend_name = fields.Str(missing=None,
                           validate = validate.Length(min = 3, max = 255))


class RequestFriendMutualSchema(Schema):
  friend_id = fields.Str(required=True,
                         validate = validate.Length(equal = 22))


class RequestFriendAddSchema(Schema):
  friend_id = fields.Str(required=True,
                         validate = validate.Length(equal = 22))


class RequestFriendAcceptRequestSchema(Schema):
  friend_request_id = fields.Int(required=True)


class RequestFriendIgnoreRequestSchema(Schema):
  friend_request_id = fields.Int(required=True)


# Responses
class FriendList(Schema):
  friend_id = fields.Str(data_key="friendID")
  user_name = fields.Str(data_key="userName")
  profile_photo = fields.Str(data_key="profilePhoto")
  avatar_num = fields.Str(data_key="avatarNum")


class FriendRequest(Schema):
  friend_request_id = fields.Str(data_key="friendRequestID")
  user_name = fields.Str(data_key="userName")
  time_diff = fields.Str(data_key="timeDiff")


class ResponseFriendListSchema(Schema):
  friend_list = fields.List(fields.Nested(FriendList), data_key="friendList")


class ResponseFriendRequestListSchema(Schema):
  friend_request_list = fields.List(fields.Nested(FriendRequest), data_key="friendRequestList")


class ResponseFriendMutualSchema(Schema):
  is_mutual = fields.Bool(data_key="isMutual")
