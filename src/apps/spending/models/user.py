from typing import List

from extension.mysql_client import db


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

    @classmethod
    def add_user(
        cls, user_id: str, name: str, password: str, email: str
    ) -> None:
        db.session.add(
            cls(id=user_id, name=name, password=password, email=email)
        )
        db.session.commit()

    @classmethod
    def show_users(cls) -> list:
        return [{
            "name": user.name,
            "password": user.password,
            "email": user.email
        } for user in cls.query.all()]
