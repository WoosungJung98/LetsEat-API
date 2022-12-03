from flask import current_app as app
from main import db
from sqlalchemy import ForeignKey


t_review = db.Table(
    "review",
    db.Column("review_id", db.String(22), primary_key=True),
    db.Column("user_id", db.String(22), ForeignKey(f"{app.config['SCHEMA_FACEYELP']}.user.user_id"), nullable=False),
    db.Column("business_id", db.String(22), ForeignKey(f"{app.config['SCHEMA_FACEYELP']}.business.business_id"), nullable=False),
    db.Column("stars", db.Integer, nullable=False),
    db.Column("body", db.Text),
    db.Column("useful", db.Integer, nullable=False),
    db.Column("funny", db.Integer, nullable=False),
    db.Column("cool", db.Integer, nullable=False),
    db.Column("created_at", db.DateTime, nullable=False),
    db.Column("updated_at", db.DateTime, nullable=False),
    schema=app.config["SCHEMA_FACEYELP"],
    extend_existing=True)
