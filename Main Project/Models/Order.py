from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
from Models.Customer import Customer

Base = declarative_base()

class Order(Base):
    __tablename__ = 'order'

    orderid = Column(Integer, primary_key=True, autoincrement=True)
    orderdate = Column(DateTime, default=datetime.datetime.utcnow)
    totalamount = Column(Float)
    customerid = Column(Integer, ForeignKey(Customer.Customerid))
    
    customer = relationship(Customer, backref='order')

    def __repr__(self):
        return f"<Order( orderdate={self.orderdate}, totalamount={self.totalamount}, customerid={self.customerid})>"
