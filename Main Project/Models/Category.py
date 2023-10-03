from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
from Models.Admin import Admin
Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'

    categoryid = Column(Integer, primary_key=True, autoincrement=True)
    categoryname = Column(String)
    adminid = Column(Integer, ForeignKey(Admin.adminid))
    
    admin = relationship(Admin, backref='category')
    def __repr__(self):
        return f"<Category( categoryname={self.categoryname})>"
