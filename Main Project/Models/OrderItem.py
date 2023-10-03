from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from Models.Product import Product
from Models.Order import Order
from Models.Sale import Sale


Base = declarative_base()


class OrderItem(Base):
    __tablename__ = 'orderitem'

    orderitemid = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer)
    subtotal = Column(Float)
    productid = Column(Integer, ForeignKey(Product.productid))
    orderid = Column(Integer, ForeignKey(Order.orderid))
    saleid = Column(Integer, ForeignKey(Sale.saleid))
    
    product = relationship(Product, backref='orderitem')
    order = relationship(Order, backref='orderitem')
    sale = relationship(Sale, backref='orderitem')

    def __repr__(self):
        return f"<OrderItem( quantity={self.quantity}, subtotal={self.subtotal}, productid={self.productid}, orderid={self.orderid}, saleid={self.saleid})>"

