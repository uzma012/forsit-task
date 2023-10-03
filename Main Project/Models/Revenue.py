from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
from Models.Order import Order

Base = declarative_base()
class Revenue(Base):
    __tablename__ = 'revenue'

    revenueid = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    amount = Column(Float)
    orderid = Column(Integer, ForeignKey(Order.orderid))

    order = relationship(Order, backref='revenue')

    def __repr__(self):
        return f"<Revenue( date={self.date}, amount={self.amount}, orderid={self.orderid})>"
