from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from Models.Product import Product
from Models.InventoryHistory import InventoryHistory
from Models.InventoryTransaction import InventoryTransaction
from datetime import datetime
from sqlalchemy import func
from sqlalchemy import and_
from sqlalchemy.orm import aliased
from sqlalchemy import select
from DTOs.InventoryResponse import InventoryResponse
from sqlalchemy.exc import IntegrityError


Base = declarative_base()


class InventoryServices:
    def __init__(self, db_manager,session):
        self.db_manager=db_manager
        self.session=session

    def view_inventory_status(self, low_stock_threshold=10):
            products = self.session.query(Product.productid, Product.productname, Product.quantityinstock).all()
            inventory_list=[]
            for product_id, product_name, quantity in products:
                status = "Low Stock Alert!" if quantity < low_stock_threshold else "Sufficient Stock"
                inventory_response = InventoryResponse(
                        product_id=product_id, 
                        product_name=product_name,  
                        quantity=quantity,
                        status=status
                )              
                inventory_list.append(inventory_response)
            self.db_manager.close_session(self.session)
            return inventory_list
        
    def update_inventory(self, product_id, quantity_changed, transaction_type,adminId):
        
        # Update the inventory for the specified product
        product = self.session.query(Product).filter(Product.productid == product_id).one_or_none()

        if product:
            # Update the quantity in stock based on the transaction type
            if transaction_type == 'Purchase':
                product.quantityinstock += quantity_changed
            elif transaction_type == 'Sale':
                product.quantityinstock -= quantity_changed

            # Record the inventory change in the history table
            inventory_history = InventoryHistory(
                productid=product_id,
                quantitychanged=quantity_changed,
                transactiontype=transaction_type,
                transactiondate=datetime.now()  # Assuming you want to record the current date and time
            )
            self.session.add(inventory_history)

            # Update the inventory table
            inventory_record = self.session.query(InventoryTransaction).filter(InventoryTransaction.productid == product_id).one_or_none()
            if not inventory_record:
                # Create a new inventory record if it doesn't exist
                inventory_record = InventoryTransaction(productid=product_id, 
                                                        quantity=product.quantityinstock,
                                                        adminId=adminId,
                                                        transactiontype =transaction_type,
                                                        transactiondate=datetime.utcnow()
                                                        )
                self.session.add(inventory_record)
            else:
                # Update the existing inventory record
                inventory_record.adminid=adminId
                inventory_record.transactiondate=datetime.utcnow()
                inventory_record.quantitychanged = product.quantityinstock

            self.session.commit()
            self.db_manager.close_session(self.session)
            return True


    def register_new_product(self, product_name, description, price, quantity_in_stock, transaction_type, admin_id,category_id):
        # try:
            # Check if the product already exists based on product name
            existing_product = self.session.query(Product).filter(Product.productname == product_name).one_or_none()

            if existing_product:
                # Product already exists, update its details
                existing_product.description = description
                existing_product.price = price
                existing_product.quantityinstock += quantity_in_stock
            else:
                # Product is new, create a new Product instance
                new_product = Product(
                    productname=product_name,
                    description=description,
                    price=price,
                    quantityinstock=quantity_in_stock,
                    adminid=admin_id,
                    categoryid=category_id
                )
            self.session.add(new_product)

            # Record the inventory transaction
            inventory_transaction = InventoryTransaction(
                transactiondate=datetime.utcnow(),
                transactiontype=transaction_type,
                quantitychanged=quantity_in_stock,
                product=existing_product if existing_product else new_product,
                adminid=admin_id
            )
            # self.session.add(inventory_transaction)

            # Update the inventory table
            product = existing_product if existing_product else new_product
            inventory_record = self.session.query(InventoryTransaction).filter(InventoryTransaction.productid == product.productid).one_or_none()
            if not inventory_record:
                inventory_record = inventory_transaction
                self.session.add(inventory_record)
            else:
                inventory_record.quantitychanged = product.quantityinstock

            self.session.commit()
            self.db_manager.close_session(self.session)

            return True

        # except IntegrityError as i:
        #     print(i.detail)
        #     self.session.rollback()
        #     self.db_manager.close_session(self.session)
        #     return False

        # except Exception as e:
        #     # print(e.message)
        #     self.session.rollback()
        #     self.db_manager.close_session(self.session)
        #     return False