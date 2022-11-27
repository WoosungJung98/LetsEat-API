from marshmallow import fields, Schema, validate, ValidationError
from main.controllers.common.date import convert_datetime, DATETIME_PATTERN
from datetime import datetime


def create_pagination_list_schema(nested_cls):
  class PaginationList(Schema):
    list = fields.List(fields.Nested(nested_cls), required=True)
    totalLength = fields.Int(attribute="total_length", required=True, validate=validate.Range(min=0))
    page = fields.Int(required=True, validate=validate.Range(min=1))

  return PaginationList


class RequestPagination(Schema):
  page = fields.Int(missing=1,
                    validate=validate.Range(min=1),
                    description="Page Number")
  length = fields.Int(missing=10, description="Number of Items per Page")


# Custom Fields

class DateTime(fields.Field):
  def _serialize(self, value, attr, obj, **kwargs):
    if not isinstance(value, datetime):
      raise ValidationError("Value to serialize must be of datetime type!")
    return convert_datetime(value)

  def _deserialize(self, value, attr, data, **kwargs):
    if not isinstance(value, str):
      raise ValidationError("Value to deserialize must be of string type!")
    return datetime.strptime(value, DATETIME_PATTERN)
