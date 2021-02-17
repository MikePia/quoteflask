"""
Get the MySql connection from a local sqlite db
"""
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from localconfig import sqlitedb

Base = declarative_base()
Session = sessionmaker()


class Keys(Base):
    __tablename__ = "keys"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    key = Column(String)

    @classmethod
    def getSAConn(self):
        # s = Session(bind=create_engine("sqlite:///c:\\python\\E\\uw\\stockquote\\keys.sqlite"))
        s = Session(bind=create_engine(sqlitedb))
        keys = s.query(Keys).all()
        k = {x.name: x.key for x in keys}
        return f'mysql+pymysql://{k["mysql_user"]}:{k["mysql_pw"]}@{k["mysql_ip"]}/{k["mysql_db"]}'


if __name__ == '__main__':
    print(Keys.getSAConn())
