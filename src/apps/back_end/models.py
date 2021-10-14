from extension.mysql_client import db


class RecordSpending(db.Model):
    __tablename__ = 'record_spending'
    id = db.Column(db.String(32), nullable=True)

    title = db.Column(db.String(100), nullable=True)
    money = db.Column(db.Float(), nullable=True)
    start_time = db.Column(db.String(100), nullable=True)
    people = db.Column(db.String(10), nullable=True)

    def show(self):
        return {
            'title': self.title,
            'id': self.money,
            'start': self.time,
            'className': self.people
        }
