from flask import current_app as app
from main import db
from sqlalchemy.dialects.postgresql import insert


t_user = db.Table(
    "user",
    db.Column("user_id", db.String(22), primary_key=True),
    db.Column("user_name", db.String(255), nullable=False),
    db.Column("email", db.String(255), unique=True, nullable=False),
    db.Column("profile_photo", db.String(22)),
    db.Column("password_digest", db.LargeBinary),
    db.Column("review_count", db.Integer, nullable=False),
    db.Column("useful", db.Integer, nullable=False),
    db.Column("funny", db.Integer, nullable=False),
    db.Column("cool", db.Integer, nullable=False),
    db.Column("created_at", db.DateTime, nullable=False),
    db.Column("updated_at", db.DateTime, nullable=False),
    schema=app.config["SCHEMA_FACEYELP"],
    extend_existing=True)


def get_user(user_id):
  query = db.select(t_user)\
    .where(t_user.c.user_id == user_id)
  return db.session.execute(query).fetchone()


def get_user_by_email(email):
  query = db.select(t_user)\
    .where(t_user.c.email == email)
  return db.session.execute(query).fetchone()


def upsert_user(upsert_dict):
  insert_stmt = insert(t_user).values(upsert_dict)

  do_nothing_stmt = insert_stmt.on_conflict_do_nothing(
      index_elements=[t_user.c.user_id, t_user.c.email]
  ).returning(t_user.c.user_id)

  db.session.execute(do_nothing_stmt)
  db.session.commit()
