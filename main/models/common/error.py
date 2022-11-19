from marshmallow import fields, Schema


class Error:
  def __init__(self, id, msg, code):
    self.id = id
    self.msg = msg
    self.code = code

  def get_response(self, **msg_kwargs):
    msg = self.msg.format(**msg_kwargs)
    return {"msg_id": self.id, "msg": msg}, self.code


class ResponseError(Schema):
  msg_id = fields.Str(data_key="msgID")
  msg = fields.Str()


ERROR_LIST_PAGE_INVALID = Error("u001", "Page must be larger than 0.", 400)
ERROR_LIST_LENGTH_INVALID = Error("u002", "Length must be positive or 0.", 400)

ERROR_BUSINESS_ID_NOT_EXISTS_PATH = Error("u101", "Specified Business ID Does Not Exist!", 404)

ERROR_INVALID_CREDENTIALS = Error("u201", "Invalid username or password!", 401)
SUCCESS_LOGOUT = Error("u202", "Log out success.", 200)
SUCCESS_CHANGE_PASSWORD = Error("u203", "Change password success.", 200)
ERROR_PASSWORD_CONFIRMATION = Error("u204", "Password confirmation failure!", 422)
ERROR_EMAIL_PATTERN_INVALID = Error("u205", "Email is formatted incorrectly!", 422)
ERROR_FAILED_ACCOUNT_CREATION = Error("u206", "Account creation failed!", 409)
SUCCESS_ACCOUNT_CREATION = Error("u207", "Account successfully created!", 200)
ERROR_EMAIL_INVALID = Error("u208", "Given email address is invalid or already exists in database!", 409)
SUCCESS_EMAIL_VALID = Error("u209", "Given email address is valid and usable", 200)
