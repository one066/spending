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

    def show(self):
        start_time = self.start_time[5:16]
        return [self.people, self.title, self.price, start_time, self.id]

    @classmethod
    def get_users(cls):
        users = [record_spending.people for record_spending in cls.query.all()]
        return list(set(users))

    @classmethod
    def get_dates(cls):
        dates = db.session.query(
            func.date_format(cls.start_time,
                             '%Y-%m-%d').label('date')).group_by('date').all()
        return [date[0] for date in dates]

    @classmethod
    def get_status(cls):
        status = db.session.query(cls.status).group_by(cls.status).all()
        return [st[0] for st in status]

    @classmethod
    def get_pie_dates(cls, status):
        users = db.session.query(
            cls.status, cls.people,
            func.sum(cls.price).label('value')).group_by(
                cls.people, cls.status).having(cls.status == status).all()
        return [{
            'name': user.people,
            'value': '%.2f' % user.value
        } for user in users]

    @classmethod
    def get_line_dates(cls, status):
        series = []
        for user in cls.get_users():
            user_data = []
            for date in cls.get_dates():
                records = cls.query.filter(
                    cls.status == status, cls.people == user,
                    cls.start_time.like(f'{date}%')).all()
                user_data.append(0 if not records else sum(
                    [float('%.2f' % record.price) for record in records]))
            series.append({
                'name': user,
                'type': 'line',
                'stack': 'Total',
                'data': user_data
            })
        return series


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
