from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
)
from main import db
from main.models.user import t_user, get_user
import bcrypt


def get_access_jwt(user_id):
  access_token = create_access_token(identity=user_id)
  return access_token


def get_jwt_by_login(user_id):
  access_token = get_access_jwt(user_id)
  refresh_token = create_refresh_token(identity=user_id)
  return access_token, refresh_token


def get_refresh_jwt(user_id):
  refresh_token = create_refresh_token(identity=user_id)
  return refresh_token


class Account():
  def __init__(self, user_id):
    self.user_id = user_id

  def authenticate(self, password):
    user = get_user(self.user_id)
    # If password is empty anybody can login
    if not user.password_digest:
      return True
    return bcrypt.checkpw(password.encode("utf-8"), user.password_digest)


  def change_password(self, old_password, new_password):
    if not self.authenticate(old_password):
      return False
    salt = bcrypt.gensalt()
    hashed_new_pw = bcrypt.hashpw(new_password.encode("utf-8"), salt)
    query = db.update(t_user)\
      .where(t_user.c.user_id == self.user_id)\
      .values(password_digest=hashed_new_pw)
    db.session.execute(query)
    db.session.commit()
    return True
