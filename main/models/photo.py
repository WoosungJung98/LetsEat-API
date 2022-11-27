from flask import current_app as app
from main import db


t_photo = db.Table(
    "photo",
    db.Column("photo_id", db.String(22), primary_key=True),
    db.Column("business_id", db.String(22)),
    db.Column("caption", db.String(255)),
    db.Column("label", db.String(255)),
    schema=app.config["SCHEMA_FACEYELP"],
    extend_existing=True)
