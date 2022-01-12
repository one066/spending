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
        """通过 status 对user spending 进行分组"""
        group_spending = db.session.query(
            cls.status, cls.people,
            func.sum(cls.price).label('value')).group_by(
                cls.people, cls.status).having(cls.status == status).all()

        return group_spending

    @classmethod
    def get_time_desc_spending(cls, status) -> List:
        """通过 status 的到降序的开支列表"""
        return cls.query.filter_by(status=status).order_by(
            cls.start_time.desc()).all()

    @classmethod
    def get_status(cls) -> List:
        """得到所有 status"""
        status = db.session.query(cls.status).group_by(cls.status).all()
        return [_st.status for _st in status]
