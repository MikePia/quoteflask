"""
SqlAlchemy model for Schedule table
"""
import datetime as dt

from sqlalchemy import create_engine, Column, Float, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from models.dbconnection import Keys
# from models.dbconnection import Keys

Base = declarative_base()
Session = sessionmaker()


class Schedule(Base):
    __tablename__ = 'quoteschedule'
    id = Column(Integer, primary_key=True)

    start = Column(DateTime, unique=True, nullable=False)
    end = Column(DateTime, unique=True, nullable=False)
    freq = Column(Float, nullable=False)

    def __repr__(self):
        if self.start:
            return f"<Schedule.quoteschedule>{self.start.strftime('%d/%m/%y %H:%M:%S')}-{self.end.strftime('%d/%m/%y %H:%M:%S')}. {self.freq} Seconds"
        return "<Schedule.quoteschedule>"

    @classmethod
    def addJob(cls, start, end, freq, engine):
        s = Session(bind=engine)
        if not Schedule.noOverlapConstraint(start, end, s, engine):
            return "Bad or conflicting times."
        qs = Schedule(start=start, end=end, freq=freq)
        s.add(qs)
        s.commit()
        return 'OK'

    @classmethod
    def removeJob(cls, start, end, engine):
        s = Session(bind=engine)
        q = s.query(Schedule).filter_by(start=start).filter_by(end=end).one_or_none()
        if q:
            s.delete(q)
            s.commit()

    @classmethod
    def getCurrentJob(cls, engine, d=None):
        s = Session(bind=engine)
        n = d if d else dt.datetime.now()
        return s.query(Schedule).filter(Schedule.start <= n).filter(Schedule.end >= n).one_or_none()

    @classmethod
    def getNextJob(cls, engine, d=None):
        s = Session(bind=engine)
        n = d if d else dt.datetime.now()
        return s.query(Schedule).filter(Schedule.end <= n).order_by(Schedule.start).first()

    @classmethod
    def noOverlapConstraint(cls, start, end, session, engine):
        '''
        Check whether start and end overlap any existing job. Returns False if there
        is a conflict and True if there is no conflict.
        '''
        jobs = session.query(Schedule).all()
        for j in jobs:
            if (start >= j.start and start <= j.end) or (end >= j.start and end <= j.end) or (
                    start <= j.start and end >= j.start) or (start >= end):
                return False
        return True


class ManageQuoteSchedule:
    def __init__(self, db, create=False):
        self.db = db
        self.engine = create_engine(self.db)
        if create:
            self.createTables()

    def createTables(self):
        # s = Session(bind=self.engine)
        Base.metadata.create_all(self.engine)


def testSchedule():
    # mq = ManageQuoteSchedule(Keys.getSAConn(), create=True)
    jobs = [
        [dt.datetime(2021, 1, 1, 12, 0, 0),  dt.datetime(2021, 1, 1, 12, 15, 0), 3],
        [dt.datetime(2021, 1, 1, 12, 30, 0), dt.datetime(2021, 1, 1, 12, 45, 0), 4],
        [dt.datetime(2021, 1, 1, 13, 0, 0),  dt.datetime(2021, 1, 1, 13, 15,  0), 5],
        [dt.datetime(2021, 1, 1, 13, 30, 0), dt.datetime(2021, 1, 1, 13, 45,  0), 1.5],
        [dt.datetime(2021, 1, 1, 14, 0, 0),  dt.datetime(2021, 1, 1, 14, 15,  0), .7],
        [dt.datetime(2021, 1, 1, 14, 30, 0), dt.datetime(2021, 1, 1, 14, 45,  0), 2.5],
        [dt.datetime(2021, 1, 1, 15, 0, 0),  dt.datetime(2021, 1, 1, 15, 15,  0), 0.6],
        [dt.datetime(2021, 1, 1, 15, 30, 0), dt.datetime(2021, 1, 1, 15, 45,  0), 12],
        [dt.datetime(2021, 1, 1, 16, 0, 0),  dt.datetime(2021, 1, 1, 16, 15,  0), 1],
        [dt.datetime(2021, 1, 1, 16, 30, 0), dt.datetime(2021, 1, 1, 16, 45,  0), 2]
    ]
    mq = ManageQuoteSchedule(Keys.getSAConn())
    for job in jobs:
        # print(job)
        print(Schedule.addJob(job[0], job[1], job[2], mq.engine))

    print(Schedule.getCurrentJob(mq.engine))
    print(Schedule.getCurrentJob(mq.engine, dt.datetime(2021, 1, 1, 12, 3, 0)))
    print(Schedule.getNextJob(mq.engine))
    print(Schedule.getNextJob(mq.engine, dt.datetime(2021, 1, 1, 12, 3, 0)))


if __name__ == '__main__':
    print(Schedule)    