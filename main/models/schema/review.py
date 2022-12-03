from marshmallow import Schema, fields, validate
from main.controllers.common.date import DATETIME_PATTERN
from main.models.common.common import (
    RequestPagination,
    create_pagination_list_schema
)

# Requests
class RequestRestaurantReviewListSchema(RequestPagination):
    stars = fields.Integer(missing = None,
                           validate = validate.Range(min = 0, max = 5))


class RequestRestaurantReviewCreateSchema(Schema):
    body = fields.Str(required = True)
    stars = fields.Integer(required = True,
                           validate = validate.Range(min = 0, max = 5))


# Responses
class ReviewListItem(Schema):
    user_name = fields.Str(data_key="userName")
    stars = fields.Int()
    body = fields.Str()
    useful = fields.Int()
    funny = fields.Int()
    cool = fields.Int()
    created_at = fields.DateTime(format=DATETIME_PATTERN, data_key="createdAt")


class ResponseRestaurantReviewListSchema(Schema):
    review = fields.Nested(
        create_pagination_list_schema(ReviewListItem),
        required=True
    )
