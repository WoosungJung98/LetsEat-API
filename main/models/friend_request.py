from flask import current_app as app
from main import db


t_friend_request = db.Table(
    "friend_request",
    db.Column("friend_request_id", db.Integer, primary_key=True),
    db.Column("user_id", db.String(22), nullable=False),
    db.Column("friend_id", db.String(22), nullable=False),
    db.Column("created_at", db.DateTime, nullable=False),
    db.Column("accepted_at", db.DateTime),
    db.Column("ignored_at", db.DateTime),
    schema=app.config["SCHEMA_FACEYELP"],
    extend_existing=True)
