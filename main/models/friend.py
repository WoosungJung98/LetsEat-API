from flask import current_app as app
from main import db


t_friend = db.Table(
    "friend",
    db.Column("user_id", db.String(22), primary_key=True),
    db.Column("friend_id", db.String(22), primary_key=True),
    db.Column("viewed_at", db.DateTime),
    schema=app.config["SCHEMA_FACEYELP"],
    extend_existing=True)
