from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from Models.Category import Category
from Models.Admin import Admin
Base = declarative_base()

class Product(Base):
    __tablename__ = 'product'

    productid = Column(Integer, primary_key=True, autoincrement=True)
    productname = Column(String)
    description = Column(String)
    price = Column(Float)
    quantityinstock = Column(Integer)
    categoryid = Column(Integer, ForeignKey(Category.categoryid))
    adminid = Column(Integer, ForeignKey(Admin.adminid))
    
    category = relationship(Category, backref='product')
    admin = relationship(Admin, backref='product')

    def __repr__(self):
        return f"<Product( productid={self.productid},productname={self.productname}, price={self.price}, quantityinstock={self.quantityinstock}, categoryid={self.categoryid}, adminid={self.adminid})>"
