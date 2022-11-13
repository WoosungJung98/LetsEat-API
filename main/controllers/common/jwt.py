from functools import wraps
from flask_jwt_extended import get_jwt_identity

from main.models.user import get_user


def check_jwt_user(fn):
  @wraps(fn)
  def wrapper(*args, **kwargs):
    user_id = get_jwt_identity()

    user = get_user(user_id)
    if not user:
      return {}, 401

    kwargs["user"] = user
    return fn(*args, **kwargs)
  return wrapper
