from flask import current_app as app
from main import db


t_meal = db.Table(
    "meal",
    db.Column("meal_id", db.Integer, primary_key=True),
    db.Column("user_id", db.String(22), nullable=False),
    db.Column("friend_id", db.String(22), nullable=False),
    db.Column("restaurant_id", db.String(22), nullable=False),
    db.Column("meal_at", db.DateTime, nullable=False),
    db.Column("created_at", db.DateTime, nullable=False),
    schema=app.config["SCHEMA_FACEYELP"],
    extend_existing=True)
