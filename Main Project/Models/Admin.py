from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Admin(Base):
    __tablename__ = 'admin'

    adminid = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)

    def __repr__(self):
        return f"<Admin(name={self.name}, email={self.email}, phone={self.phone})>"
