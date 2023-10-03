from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from Models.Admin import Admin
from Models.DBContext import DatabaseManager
from Models.Sale import Sale
from Models.Product import Product
from Models.Order import Order
from Models.Category import Category
from Models.OrderItem import OrderItem
from Models.Revenue import Revenue
import datetime
from sqlalchemy import func
from datetime import datetime, timedelta
from sqlalchemy import and_
from sqlalchemy.orm import aliased
from sqlalchemy import select

Base = declarative_base()

class ProductService:
    def __init__(self, db_manager,session):
        self.db_manager=db_manager
        self.session=session
    
    def register_new_product(self, product_name, description, price, quantity_in_stock, category_id, admin_id):
        # Create a new Product instance
        new_product = Product(
            productname=product_name,
            description=description,
            price=price,
            quantityinstock=quantity_in_stock,
            categoryid=category_id,
            adminid=admin_id
        )

        # Add the new product to the database
        self.session.add(new_product)
        self.session.commit()
        self.db_manager.close_session(self.session)