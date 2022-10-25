from marshmallow import fields, Schema, validate


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
  length = fields.Int(missing=0, description="Number of Items per Page")
