from typing import List

from sqlalchemy import func
from sqlalchemy.engine import Row

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
    def get_spending_group_by_user(cls, status) -> List[Row]:
        """通过 status 对user spending 进行分组"""
        group_spending = db.session.query(
            cls.status, cls.people,
            func.sum(cls.price).label('value')
        ).group_by(cls.people, cls.status).having(cls.status == status).all()

        return group_spending

    @classmethod
    def get_time_desc_spending(cls, status) -> List[Row]:
        """通过 status 的到降序的开支列表"""
        return cls.query.filter_by(status=status
                                  ).order_by(cls.start_time.desc()).all()

    @classmethod
    def get_status(cls, remove_now_mouth: bool = False) -> List[str]:
        """得到所有 status"""
        status = db.session.query(cls.status).group_by(cls.status).all()
        status = [_st.status for _st in status]
        if remove_now_mouth and '暂无' in status:
            status.remove('暂无')
        return status

    @classmethod
    def get_dates_by_status(cls, status: str) -> List[str]:
        """通过 status 得到 dates"""
        dates = db.session.query(
            func.date_format(cls.start_time, '%Y-%m-%d').label('date')
        ).group_by('date').filter(cls.status == status
                                 ).order_by(cls.start_time.asc()).all()

        return [date.date for date in dates]

    @classmethod
    def get_user_spending_by_date(cls, user, dates, status) -> List[float]:
        """得到user每天的 spending"""
        user_spending_by_date = []
        for date in dates:
            # 得到 user 当天 所有开支
            records = cls.query.filter(
                cls.status == status, cls.people == user,
                cls.start_time.like(f'{date}%')
            ).order_by(cls.start_time.desc()).all()

            # 计算 user 当天总开支
            user_date_spending = '%.2f' % sum(
                float(record.price) for record in records
            ) if records else 0

            user_spending_by_date.append(user_date_spending)
        return user_spending_by_date

    @classmethod
    def get_now_mouth_users_spending(cls) -> List[Row]:
        """得到当月用户开支"""
        return db.session.query(
            cls.title, cls.people, cls.price, cls.start_time
        ).filter_by(status='暂无').all()

    @classmethod
    def end_spending_for_the_mouth(cls, now_mouth_title) -> None:
        """结束当月开支"""
        cls.query.filter(cls.status == '暂无').update({'status': now_mouth_title})
        db.session.commit()
