from typing import List

from sqlalchemy import func

from extension.mysql_client import db


class RecordSpending(db.Model):
    __tablename__ = 'record_spending'
    id = db.Column(db.String(32), nullable=True, primary_key=True)

    title = db.Column(db.String(100), nullable=True)
    price = db.Column(db.Float(), nullable=True)
    start_time = db.Column(db.String(100), nullable=True)
    people = db.Column(db.String(10), nullable=True)
    status = db.Column(db.String(50))

    def show(self) -> List:
        start_time = self.start_time[5:16]
        return [self.people, self.title, self.price, start_time, self.id]

    @classmethod
    def get_spending_group_by_user(cls, status) -> List:
        group_spending = db.session.query(
            cls.status, cls.people,
            func.sum(cls.price).label('value')).group_by(
                cls.people, cls.status).having(cls.status == status).all()
        return group_spending


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.String(32), nullable=True)
    name = db.Column(db.String(50), nullable=True, primary_key=True)
    password = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(20), nullable=True)

    def login(self, password) -> bool:
        return self.password == password

    @classmethod
    def emails(cls) -> List[str]:
        return [user.email for user in cls.query.all()]

    @classmethod
    def names(cls) -> List[str]:
        return [user.name for user in cls.query.all()]
