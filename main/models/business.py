from flask import current_app as app
from main import db
from sqlalchemy.dialects.postgresql import ARRAY, JSON


t_business = db.Table(
    "business",
    db.Column("business_id", db.String(22), primary_key=True),
    db.Column("business_name", db.String(255), nullable=False),
    db.Column("address", db.String(255), nullable=False),
    db.Column("city", db.String(255), nullable=False),
    db.Column("state", db.String(2)),
    db.Column("postal_code", db.String(255)),
    db.Column("latitude", db.Float, nullable=False),
    db.Column("longitude", db.Float, nullable=False),
    db.Column("stars", db.Float, nullable=False),
    db.Column("review_count", db.Integer, nullable=False),
    db.Column("is_open", db.Boolean, nullable=False),
    db.Column("attributes", JSON),
    db.Column("categories", ARRAY(db.String(255)), nullable=False),
    db.Column("hours", db.JSON),
    schema=app.config["SCHEMA_FACEYELP"],
    extend_existing=True)
