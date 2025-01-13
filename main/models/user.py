from flask import current_app as app
from main import db
from sqlalchemy.dialects.postgresql import insert


t_user = db.Table(
    "user",
    db.Column("user_id", db.String(22), primary_key=True),
    db.Column("user_name", db.String(255), nullable=False),
    db.Column("email", db.String(255), unique=True, nullable=False),
    db.Column("avatar_num", db.Integer),
    db.Column("password_digest", db.LargeBinary),
    db.Column("created_at", db.DateTime, nullable=False),
    db.Column("updated_at", db.DateTime, nullable=False),
    schema=app.config["SCHEMA_FACEYELP"],
    extend_existing=True)


t_user_name_cnt_map = db.Table(
    "user_name_cnt_map",
    db.Column("user_name", db.String(255), primary_key=True),
    db.Column("cnt", db.Integer, nullable=False),
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


def upsert_user_name_cnt_map(upsert_dict):
  insert_stmt = insert(t_user_name_cnt_map).values(upsert_dict)
  excl_col_dict = {
      "cnt": t_user_name_cnt_map.c.cnt + 1
  }
  upsert_col_names = [key.name for key in upsert_dict]

  do_update_stmt = insert_stmt.on_conflict_do_update(
      index_elements=[t_user_name_cnt_map.c.user_name],
      set_={key: excl_col_dict[key] for key in excl_col_dict if key in upsert_col_names}
  )
  db.session.execute(do_update_stmt)
  db.session.commit()
