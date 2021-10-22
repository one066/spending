from marshmallow import Schema, fields


class AddSpendingValidator(Schema):
    title = fields.Str(required=True)
    price = fields.Float(required=True)


class LoginValidator(Schema):
    name = fields.Str(required=True)
    password = fields.Str(required=True)