from flask_apispec import use_kwargs, marshal_with, doc
from sqlalchemy import func
from main import db
from main.controllers.user import user_bp, API_CATEGORY
from main.controllers.common.common import gen_random_uid
from main.models.schema.user import (
    RequestCreateAccountSchema,
    RequestVerifyEmailSchema
)
from main.models.user import (
    t_user,
    t_user_name_cnt_map,
    upsert_user,
    upsert_user_name_cnt_map,
    get_user_by_email
)
from main.models.common.error import (
    ResponseError,
    ERROR_PASSWORD_CONFIRMATION,
    ERROR_EMAIL_PATTERN_INVALID,
    ERROR_FAILED_ACCOUNT_CREATION,
    SUCCESS_ACCOUNT_CREATION,
    ERROR_EMAIL_ALREADY_TAKEN,
    SUCCESS_EMAIL_AVAILABLE
)
import re
import bcrypt

EMAIL_REGEX = """(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""


@user_bp.route("/create", methods=["POST"])
@use_kwargs(RequestCreateAccountSchema)
@marshal_with(ResponseError)
@doc(tags=[API_CATEGORY],
     summary="User Create",
     description="Create account for a new user")
def user_create(user_name, email, password, password_confirm, avatar_num):
  if password != password_confirm:
    return ERROR_PASSWORD_CONFIRMATION.get_response()
  regex_pattern = re.compile(EMAIL_REGEX)
  if not re.fullmatch(regex_pattern, email):
    return ERROR_EMAIL_PATTERN_INVALID.get_response()
  if get_user_by_email(email):
    return ERROR_EMAIL_ALREADY_TAKEN.get_response()
  
  random_uid = None
  while True:
    random_uid = gen_random_uid()
    query = db.session.query(t_user.c.user_id).filter(t_user.c.user_id == random_uid)
    try
      insert
      break
    except
      continue

    if not db.session.query(query.exists()).scalar():
      break

  salt = bcrypt.gensalt()
  hashed_pw = bcrypt.hashpw(password.encode("utf-8"), salt)
  
  try:
    upsert_dict = {
        t_user.c.user_id: random_uid,
        t_user.c.user_name: user_name.strip(),
        t_user.c.email: email,
        t_user.c.avatar_num: avatar_num,
        t_user.c.password_digest: hashed_pw,
        t_user.c.review_count: 0,
        t_user.c.useful: 0,
        t_user.c.funny: 0,
        t_user.c.cool: 0,
        t_user.c.created_at: func.now(),
        t_user.c.updated_at: func.now(),
    }
    upsert_user(upsert_dict)
    upsert_user_name_cnt_map({
        t_user_name_cnt_map.c.user_name: user_name.strip(),
        t_user_name_cnt_map.c.cnt: 1
    })
  except:
    return ERROR_FAILED_ACCOUNT_CREATION.get_response()

  return SUCCESS_ACCOUNT_CREATION.get_response()


@user_bp.route("/verify-email", methods=["GET"])
@use_kwargs(RequestVerifyEmailSchema, location="query")
@marshal_with(ResponseError)
@doc(tags=[API_CATEGORY],
     summary="Verify User Email",
     description="Verify email uniqueness for new user account")
def user_verify_email(email):
  if get_user_by_email(email):
    return ERROR_EMAIL_ALREADY_TAKEN.get_response()
  return SUCCESS_EMAIL_AVAILABLE.get_response()
