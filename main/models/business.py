from flask import current_app as app
from main import db
from sqlalchemy.dialects.postgresql import ARRAY, JSON


t_business = db.Table(
    "business",
    db.Column("business_id", db.String(22), primary_key=True),
    db.Column("business_name", db.String(255), nullable=False),
    db.Column("address", db.String(255), nullable=False),
    db.Column("city", db.String(255), nullable=False),
    schema=app.config["SCHEMA_FACEYELP"],
    extend_existing=True)


def get_restaurant(business_id):
  query = db.select(t_business)\
    .where(t_business.c.business_id == business_id)
  return db.session.execute(query).fetchone()
