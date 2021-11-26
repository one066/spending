from marshmallow import Schema, fields


class AddSpendingValidator(Schema):
    title = fields.Str(required=True)
    price = fields.Float(required=True)


class LoginValidator(Schema):
    name = fields.Str(required=True)
    password = fields.Str(required=True)


class LoginSerialize(Schema):
    login = fields.Bool()
    token = fields.Str()
    name = fields.Str()


class StatusValidator(Schema):
    status = fields.Str(required=True)


class PieValidator(Schema):
    status = fields.Str(required=True)
    _ = fields.Str(required=True)


class PieDataSerialize(Schema):
    data = fields.List(fields.Dict)


class ShowSpendingSerialize(Schema):
    data = fields.List(fields.List(fields.Str))


class UsersSerialize(Schema):
    users = fields.List(fields.Str)


class StatusSerialize(Schema):
    status = fields.List(fields.Str)


class LineDataSerialize(Schema):
    dates = fields.List(fields.Str)
    users = fields.List(fields.Str)
    series = fields.List(fields.Dict)
