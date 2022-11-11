from flask import current_app as app
from main import db
from sqlalchemy.dialects.postgresql import ARRAY


t_photos = db.Table(
    "photos",
    db.Column("photo_id", db.String(22)),
    db.Column("business_id", db.String(22)),
    db.Column("caption", db.String(255)),
    db.Column("label", db.String(255)),
    schema=app.config["SCHEMA_FACEYELP"],
    extend_existing=True)