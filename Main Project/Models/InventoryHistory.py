from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from Models.Product import Product
Base = declarative_base()

class InventoryHistory(Base):
    __tablename__ = 'inventoryhistory'

    transactionid = Column(Integer, primary_key=True, autoincrement=True)
    transactiondate = Column(DateTime(timezone=True), default=func.now())
    productid = Column(Integer, ForeignKey(Product.productid), nullable=False)
    quantitychanged = Column(Integer, nullable=False)
    transactiontype = Column(String, nullable=False)  # 'Purchase' or 'Sale'

    product = relationship(Product, backref='inventoryhistory')

    def __repr__(self):
        return f'<InventoryHistory( transactiondate={self.transactiondate}, ' \
               f'productid={self.productid}, quantitychanged={self.quantitychanged}, ' \
               f'transactiontype={self.transactiontype})>'
