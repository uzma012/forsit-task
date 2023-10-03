from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'Customer'

    Customerid = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(String)

    def __repr__(self):
        return f"<Customer( firstname={self.firstname}, lastname={self.lastname}, email={self.email}, phone={self.phone}, address={self.address})>"
