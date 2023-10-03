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
from typing import List, Optional
from Models.Revenue import Revenue
import datetime
from sqlalchemy import func
from sqlalchemy import extract
from datetime import datetime, timedelta
from sqlalchemy import and_
from sqlalchemy.orm import aliased
from sqlalchemy import select
from DTOs.SalesResponse import SalesResponse
from DTOs.RevenueResponse import RevenueResponse
from DTOs.RevenueDTO import RevenueDTO
from sqlalchemy.sql import select, literal_column

Base = declarative_base()

class SalesServices:
    def __init__(self, db_manager,session):
        self.db_manager=db_manager
        self.session=session

        
    def get_sales_by_date(self, start_date: str, end_date: str):
        query = self.session.query(Sale, OrderItem, Product).\
            join(OrderItem, Sale.saleid == OrderItem.saleid).\
            join(Product, OrderItem.productid == Product.productid).\
            filter(Sale.salesdate.between(start_date, end_date))

        results = query.all()

        sales_response_list = []
        for sale, order_item, product in results:
            sales_response = SalesResponse(
                sale_date=sale.salesdate.strftime('%Y-%m-%d'),
                total_sale_amount=sale.totalsaleamount,
                product_id=order_item.productid if order_item else None,
                category_id=product.categoryid if product else None
            )
            sales_response_list.append(sales_response)

        self.db_manager.close_session(self.session)
        return sales_response_list
        
    def get_sales_by_category(self, category_id: int):
            query = self.session.query(Sale, OrderItem, Product).\
                join(OrderItem, Sale.saleid == OrderItem.saleid).\
                join(Product, OrderItem.productid == Product.productid).\
                filter(Product.categoryid == category_id)

            results = query.all()

            sales_response_list = []
            for sale, order_item, product in results:
                sales_response = SalesResponse(
                    sale_date=sale.salesdate.strftime('%Y-%m-%d'),
                    total_sale_amount=sale.totalsaleamount,
                    product_id=order_item.productid if order_item else None,
                    category_id=product.categoryid if product else None
                )
                sales_response_list.append(sales_response)

            self.db_manager.close_session(self.session)
            return sales_response_list

    def get_sales_by_product(self, product_id: int):
            query = self.session.query(Sale, OrderItem, Product).\
                join(OrderItem, Sale.saleid == OrderItem.saleid).\
                join(Product, OrderItem.productid == Product.productid).\
                filter(Product.productid == product_id)

            results = query.all()

            sales_response_list = []
            for sale, order_item, product in results:
                sales_response = SalesResponse(
                    sale_date=sale.salesdate.strftime('%Y-%m-%d'),
                    total_sale_amount=sale.totalsaleamount,
                    product_id=order_item.productid if order_item else None,
                    category_id=product.categoryid if product else None
                )
                sales_response_list.append(sales_response)

            self.db_manager.close_session(self.session)
            return sales_response_list

    def get_sales_by_customer(self, customer_id):
            sales = self.session.query(Sale).filter(Sale.customerid == customer_id).all()
            self.db_manager.close_session(self.session)
            return sales
        
    def calculate_total_sales_amount(self,sales):
            total_amount = sum(sale.totalsaleamount for sale in sales)
            return total_amount  


    def calculate_revenue_daily(self,date):
        
            daily_revenue = self.session.query(func.sum(Revenue.amount)).filter(Revenue.date == date).scalar() or 0
            self.db_manager.close_session(self.session)
            return daily_revenue

    def calculate_revenue_weekly( self,start_date):
            end_date = start_date + timedelta(days=6)
    
            weekly_revenue = self.session.query(func.sum(Revenue.amount)).filter(Revenue.date.between(start_date, end_date)).scalar() or 0
            self.db_manager.close_session(self.session)
            return weekly_revenue

    def calculate_revenue_monthly(self, year, month):
            start_date = datetime(year, month, 1)
            end_date = datetime(year, month + 1, 1) - timedelta(days=1)
    
            monthly_revenue = self.session.query(func.sum(Revenue.amount)).filter(Revenue.date.between(start_date, end_date)).scalar() or 0
            self.db_manager.close_session(self.session)
            return monthly_revenue

    def calculate_revenue_annually(self, year):
            start_date = datetime(year, 1, 1)
            end_date = datetime(year, 12, 31)
    
            annual_revenue = self.session.query(func.sum(Revenue.amount)).filter(Revenue.date.between(start_date, end_date)).scalar() or 0
            self.db_manager.close_session(self.session)
            return annual_revenue


    def compare_revenue_across_periods_and_categories(self,start_date, end_date,category_id=0):
            
            # Get all categories
            
            comparison_data = []
            if category_id==0:
                categories = self.session.query(Category).all()
                for category in categories:

                    # Calculate revenue for each period
                    daily_revenue = self.calculate_revenue_daily_by_category(start_date, end_date, category.categoryid)
                    weekly_revenue = self.calculate_revenue_weekly_by_category(start_date, end_date, category.categoryid)
                    monthly_revenue = self.calculate_revenue_monthly_by_category(start_date, end_date, category.categoryid)
                    yearly_revenue = self.calculate_revenue_yearly_by_category(start_date.year, category.categoryid)
                    
                    revenue_period = RevenueDTO(
                    daily_revenue = daily_revenue,
                    weekly_revenue = weekly_revenue,
                    monthly_revenue= monthly_revenue,
                    yearly_revenue=yearly_revenue,
                    period_end_date= end_date.strftime('%Y-%m-%d'),
                    period_start_date=start_date.strftime('%Y-%m-%d'))
                    category_data = RevenueResponse (
                        category_name= category.categoryname,
                        revenue_by_period=revenue_period
                    )
                    comparison_data.append(category_data)
            else:
                categories = self.session.query(Category).filter( Category.categoryid == category_id)
                for category in categories:
                    daily_revenue = self.calculate_revenue_daily_by_category(start_date, end_date, category_id)
                    weekly_revenue = self.calculate_revenue_weekly_by_category(start_date, end_date, category_id)
                    monthly_revenue = self.calculate_revenue_monthly_by_category(start_date, end_date, category_id)
                    yearly_revenue = self.calculate_revenue_yearly_by_category(start_date.year, category_id)
                    revenue_period = RevenueDTO(
                    daily_revenue = daily_revenue,
                    weekly_revenue = weekly_revenue,
                    monthly_revenue= monthly_revenue,
                    yearly_revenue=yearly_revenue,
                    period_end_date= end_date.strftime('%Y-%m-%d'),
                    period_start_date=start_date.strftime('%Y-%m-%d'))
                    category_data = RevenueResponse (
                            category_name= category.categoryname,
                            revenue_by_period=revenue_period
                        )
                    comparison_data.append(category_data)
            self.db_manager.close_session(self.session)

            return comparison_data

    def calculate_revenue_daily_by_category(self, start_date, end_date, categoryid):

            daily_revenue = self.session.query(func.sum(Sale.totalsaleamount)).\
            join(OrderItem, OrderItem.saleid == Sale.saleid).\
            join(Product, Product.productid == OrderItem.productid).\
            join(Category, Category.categoryid == Product.categoryid).\
            filter(Sale.salesdate.between(start_date, end_date), Category.categoryid == categoryid).\
                scalar() or 0
            self.db_manager.close_session(self.session)

            return daily_revenue

    def calculate_revenue_weekly_by_category(self, start_date, end_date, categoryid):
        # Adjust start_date to the beginning of the week
        start_date -= timedelta(days=start_date.weekday())
        # Adjust end_date to the end of the week
        end_date = start_date + timedelta(days=6)
        # Calculate weekly revenue for the specified category
        weekly_revenue = self.session.query(func.sum(Sale.totalsaleamount)).\
            join(OrderItem, OrderItem.saleid == Sale.saleid).\
            join(Product, Product.productid == OrderItem.productid).\
            join(Category, Category.categoryid == Product.categoryid).\
            filter(Sale.salesdate.between(start_date, end_date), Category.categoryid == categoryid).\
            scalar() or 0

        self.db_manager.close_session(self.session)
        return weekly_revenue
    
    def calculate_revenue_yearly_by_category(self, year, categoryid):
            # Calculate start and end dates for the specified year
        start_date = datetime(year, 1, 1)  # January 1st of the specified year
        end_date = datetime(year, 12, 31)  # December 31st of the specified year
        # Calculate yearly revenue for the specified category
        yearly_revenue = self.session.query(func.sum(Sale.totalsaleamount)).\
            join(OrderItem, OrderItem.saleid == Sale.saleid).\
            join(Product, Product.productid == OrderItem.productid).\
            join(Category, Category.categoryid == Product.categoryid).\
            filter(
                Sale.salesdate.between(start_date, end_date),
                extract('year', Sale.salesdate) == year,
                Category.categoryid == categoryid
            ).\
            scalar() or 0
        self.db_manager.close_session(self.session)
        return yearly_revenue
    
    def calculate_revenue_monthly_by_category( self,start_date, end_date, categoryid):
            start_date = datetime(start_date.year, start_date.month, 1)
            end_date = datetime(end_date.year, end_date.month, 1) + timedelta(days=31)  # Allow for a full month
            monthly_revenue = self.session.query(func.sum(Sale.totalsaleamount)).\
                join(OrderItem, OrderItem.saleid == Sale.saleid).\
                join(Product, Product.productid == OrderItem.productid).\
                join(Category, Category.categoryid == Product.categoryid).\
                filter(Sale.salesdate.between(start_date, end_date), Category.categoryid == categoryid).\
                scalar() or 0
            self.db_manager.close_session(self.session)

            return monthly_revenue


    def get_sales_by_criteria(self, start_date: str, end_date: str, product_id: Optional[int] = None, category_id: Optional[int] = None):
        query = self.session.query(Sale, OrderItem, Product).\
            join(OrderItem, Sale.saleid == OrderItem.saleid).\
            join(Product, OrderItem.productid == Product.productid).\
            filter(Sale.salesdate.between(start_date, end_date))

        if product_id:
            query = query.filter(OrderItem.productid == product_id)

        if category_id:
            query = query.filter(Product.categoryid == category_id)

        results = query.all()

        sales_response_list = []
        for sale, order_item, product in results:
            sales_response = SalesResponse(
                sale_date=sale.salesdate.strftime('%Y-%m-%d'),
                total_sale_amount=sale.totalsaleamount,
                product_id=order_item.productid if order_item else None,
                category_id=product.categoryid if product else None
            )
            sales_response_list.append(sales_response)

        self.db_manager.close_session(self.session)
        return sales_response_list
        
