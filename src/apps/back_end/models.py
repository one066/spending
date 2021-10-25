from extension.mysql_client import db


class RecordSpending(db.Model):
    __tablename__ = 'record_spending'
    id = db.Column(db.String(32), nullable=True, primary_key=True)

    title = db.Column(db.String(100), nullable=True)
    price = db.Column(db.Float(), nullable=True)
    start_time = db.Column(db.String(100), nullable=True)
    people = db.Column(db.String(10), nullable=True)
    status = db.Column(db.String(50))

    def show(self):
        start_time = self.start_time[5:16]
        return [self.people, self.title, self.price, start_time, self.id]

    @classmethod
    def shows(cls):
        return [spending.show() for spending in cls.query.all()]

    @classmethod
    def get_home_echarts_data(cls):
        data = {}
        for spending in cls.query.all():
            if spending.people in data:
                data[spending.people] += spending.price
            else:
                data[spending.people] = spending.price
        return data

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.String(32), nullable=True)
    name = db.Column(db.String(50), nullable=True, primary_key=True)
    password = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(20), nullable=True)

    def login(self, password):
        return self.password == password

    @classmethod
    def emails(cls):
        return [user.email for user in cls.query.all()]