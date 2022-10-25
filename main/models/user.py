from flask import current_app as app
from main import db
from sqlalchemy.dialects.postgresql import ARRAY


t_user = db.Table(
    "user",
    db.Column("user_id", db.String(22), primary_key=True),
    db.Column("user_name", db.String(255), nullable=False),
    db.Column("profile_photo", db.String(22)),
    db.Column("password_digest", db.String(255)),
    db.Column("review_count", db.Integer, nullable=False),
    db.Column("friends", ARRAY(db.String(22)), nullable=False),
    db.Column("useful", db.Integer, nullable=False),
    db.Column("funny", db.Integer, nullable=False),
    db.Column("cool", db.Integer, nullable=False),
    db.Column("created_at", db.DateTime, nullable=False),
    db.Column("updated_at", db.DateTime, nullable=False),
    schema=app.config["SCHEMA_FACEYELP"],
    extend_existing=True)
