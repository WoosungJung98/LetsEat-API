from flask_apispec import use_kwargs, marshal_with, doc
from flask_jwt_extended import jwt_required
from main.controllers.common.jwt import check_jwt_user
from main.controllers.user import user_bp, API_CATEGORY, authorization_header
from main.models.schema.user import (
    RequestLoginSchema,
    ResponseLoginSchema,
    ResponseAccessTokenSchema,
    RequestChangePassword
)
from main.models.account import (
    Account,
    get_jwt_by_login,
    get_access_jwt,
)
from main.models.user import get_user_by_email
from main.models.common.error import (
    ResponseError,
    ERROR_INVALID_CREDENTIALS,
    SUCCESS_LOGOUT,
    SUCCESS_CHANGE_PASSWORD
)


@user_bp.route("/login", methods=["POST"])
@use_kwargs(RequestLoginSchema)
@marshal_with(ResponseError)
@marshal_with(ResponseLoginSchema, code=200)
@doc(tags=[API_CATEGORY],
     summary="User Login",
     description="Log in the user and fetch JWT tokens")
def user_login(email, password):
  user = get_user_by_email(email)
  if not user:
    return ERROR_INVALID_CREDENTIALS.get_response()
  
  account = Account(user.user_id)
  if not account.authenticate(password):
    return ERROR_INVALID_CREDENTIALS.get_response()

  access_token, refresh_token = get_jwt_by_login(user.user_id)

  return {
      "access_token": access_token,
      "refresh_token": refresh_token,
  }


@user_bp.route("/login/refresh", methods=["POST"])
@jwt_required(refresh=True)
@check_jwt_user
@marshal_with(ResponseAccessTokenSchema, code=200)
@doc(tags=[API_CATEGORY],
     summary="Refresh token",
     description="Fetch new access token using refresh token.",
     params=authorization_header)
def user_refresh(user):
  return {"access_token": get_access_jwt(user.user_id)}


@user_bp.route("/logout", methods=["POST"])
@jwt_required()
@marshal_with(ResponseError)
@doc(tags=[API_CATEGORY],
     summary="logout",
     description="Logout the user.",
     params=authorization_header)
def user_logout():
  return SUCCESS_LOGOUT.get_response()


@user_bp.route("/password", methods=["POST"])
@jwt_required()
@check_jwt_user
@use_kwargs(RequestChangePassword)
@marshal_with(ResponseError)
@doc(tags=[API_CATEGORY],
     summary="change password",
     description="Change the password.",
     params=authorization_header)
def user_change_password(user, old_password, new_password):
  account = Account(user.user_id)
  if not account.change_password(old_password, new_password):
    return ERROR_INVALID_CREDENTIALS.get_response()
  return SUCCESS_CHANGE_PASSWORD.get_response()
