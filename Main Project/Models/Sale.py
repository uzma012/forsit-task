from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
from Models.Customer import Customer

Base = declarative_base()


class Sale(Base):
    __tablename__ = 'Sale'

    saleid = Column(Integer, primary_key=True, autoincrement=True)
    salesdate = Column(DateTime, default=datetime.datetime.utcnow)
    totalsaleamount = Column(Float)
    customerid = Column(Integer, ForeignKey(Customer.Customerid))

    Customer = relationship(Customer, backref='Sale')

    def __repr__(self):
        return f"<Sale( salesdate={self.salesdate}, totalsaleamount={self.totalsaleamount}, customerid={self.customerid})>"