from marshmallow import Schema, fields


class ErrorSchema(Schema):
    message = fields.String(required=True)
    errors = fields.Raw()
    timestamp = fields.DateTime()
    status_code = fields.Integer()


class ValidationErrorSchema(Schema):
    message = fields.String(required=True)
    errors = fields.Dict(keys=fields.String(), values=fields.List(fields.String()))


error_schema = ErrorSchema()
validation_error_schema = ValidationErrorSchema()