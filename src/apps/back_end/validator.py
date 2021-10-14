from marshmallow import Schema, fields


class AddSpendingValidator(Schema):
    title = fields.Str(required=True)
    money = fields.Float(required=True)
    people = fields.Str(required=True)


class LoginValidator(Schema):
    name = fields.Str(required=True)
    password = fields.Str(required=True)