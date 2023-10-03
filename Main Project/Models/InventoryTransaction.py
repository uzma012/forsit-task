from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
from Models.Product import Product
from Models.Admin import Admin
Base = declarative_base()


class InventoryTransaction(Base):
    __tablename__ = 'inventorytransactions'

    transactionid = Column(Integer, primary_key=True, autoincrement=True)
    transactiondate = Column(DateTime, default=datetime.datetime.utcnow)
    transactiontype = Column(String)
    quantitychanged = Column(Integer)
    productid = Column(Integer, ForeignKey(Product.productid))
    adminid = Column(Integer, ForeignKey(Admin.adminid))

    product = relationship(Product, backref='inventorytransactions')
    admin = relationship(Admin, backref='inventorytransactions')

    def __repr__(self):
        return f"< transactiondate={self.transactiondate}, transactiontype={self.transactiontype}, quantitychanged={self.quantitychanged}, productid={self.productid}, adminid={self.adminid})>"
