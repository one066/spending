from marshmallow import Schema, fields


class AddSpendingValidator(Schema):
    title = fields.Str(required=True)
    price = fields.Float(required=True)


class LoginValidator(Schema):
    password = fields.Str(required=True)