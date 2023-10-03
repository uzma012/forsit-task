from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from Models.Sale import Sale
from Models.Product import Product
from Models.Category import Category
from Models.OrderItem import OrderItem
from typing import List, Optional
from Models.Revenue import Revenue
import datetime
from sqlalchemy import func
from dateutil.relativedelta import relativedelta
from sqlalchemy import extract
from datetime import datetime, timedelta
from sqlalchemy import and_
from sqlalchemy.orm import aliased
from collections import defaultdict
from sqlalchemy import func, cast, Date, text
from sqlalchemy import select
from DTOs.SalesResponse import SalesResponse
from DTOs.RevenueResponse import RevenueResponse
from DTOs.RevenueDTO import RevenueDTO
from sqlalchemy.sql import select, literal_column
import numpy as np
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


    def compare_revenue_across_periods_and_categories(self,start_date, end_date,period,category_id=0):
            
            # Get all categories
            
            comparison_data = []
            if category_id==0:
                categories = self.session.query(Category).all()
                for category in categories:
                    revenue_list = []
                    revenue = []
                    # Calculate revenue for each period
                    if period == "d":
                        revenue = self.calculate_revenue_daily_by_category(start_date, end_date, category.categoryid)
                    elif period == "w":
                        revenue = self.calculate_revenue_weekly_by_category(start_date, end_date, category.categoryid)
                    elif period =="m":
                        revenue = self.calculate_revenue_monthly_by_category(start_date, end_date, category.categoryid)
                    elif period == "y":
                        revenue = self.calculate_revenue_yearly_by_category(start_date, end_date, category.categoryid)
                    
                    for date in revenue:
                        revenue_period = RevenueDTO(
                        revenue = date[3],
                        period_end_date= date[2].strftime('%Y-%m-%d'),
                        period_start_date=date[1].strftime('%Y-%m-%d'))
                        revenue_list.append(revenue_period)
                         
                    category_data = RevenueResponse (
                        category_name= category.categoryname,
                        revenue_by_period=revenue_list
                    )
                    comparison_data.append(category_data)
            else:
                categories = self.session.query(Category).filter( Category.categoryid == category_id)
                for category in categories:
                    revenue_list = []
                    revenue = []
                    if period == "d":
                        revenue = self.calculate_revenue_daily_by_category(start_date, end_date, category.categoryid)
                    elif period == "w":
                        revenue = self.calculate_revenue_weekly_by_category(start_date, end_date, category.categoryid)
                    elif period =="m":
                        revenue = self.calculate_revenue_monthly_by_category(start_date, end_date, category.categoryid)
                    elif period == "y":
                        revenue = self.calculate_revenue_yearly_by_category(start_date, end_date, category.categoryid)
                        
                    for date in revenue:
                        revenue_period = RevenueDTO(
                        revenue = date[3],
                        period_end_date= date[2].strftime('%Y-%m-%d'),
                        period_start_date=date[1].strftime('%Y-%m-%d'))
                        revenue_list.append(revenue_period)
                         
                    category_data = RevenueResponse (
                        category_name= category.categoryname,
                        revenue_by_period=revenue_list
                    )
                    comparison_data.append(category_data)
            self.db_manager.close_session(self.session)

            return comparison_data

    # def calculate_revenue_daily_by_category(self, start_date, end_date, categoryid):

    #         daily_revenue = self.session.query(func.sum(Sale.totalsaleamount)).\
    #         join(OrderItem, OrderItem.saleid == Sale.saleid).\
    #         join(Product, Product.productid == OrderItem.productid).\
    #         join(Category, Category.categoryid == Product.categoryid).\
    #         filter(Sale.salesdate.between(start_date, end_date), Category.categoryid == categoryid).\
    #             scalar() or 0
    #         self.db_manager.close_session(self.session)

    #         return daily_revenue

    # def calculate_revenue_weekly_by_category(self, start_date, end_date, categoryid):
    #     # Adjust start_date to the beginning of the week
    #     start_date -= timedelta(days=start_date.weekday())
    #     # Adjust end_date to the end of the week
    #     end_date = start_date + timedelta(days=6)
    #     # Calculate weekly revenue for the specified category
    #     weekly_revenue = self.session.query(func.sum(Sale.totalsaleamount)).\
    #         join(OrderItem, OrderItem.saleid == Sale.saleid).\
    #         join(Product, Product.productid == OrderItem.productid).\
    #         join(Category, Category.categoryid == Product.categoryid).\
    #         filter(Sale.salesdate.between(start_date, end_date), Category.categoryid == categoryid).\
    #         scalar() or 0

    #     self.db_manager.close_session(self.session)
    #     return weekly_revenue
    
    # def calculate_revenue_yearly_by_category(self, year, categoryid):
    #         # Calculate start and end dates for the specified year
    #     start_date = datetime(year, 1, 1)  # January 1st of the specified year
    #     end_date = datetime(year, 12, 31)  # December 31st of the specified year
    #     # Calculate yearly revenue for the specified category
    #     yearly_revenue = self.session.query(func.sum(Sale.totalsaleamount)).\
    #         join(OrderItem, OrderItem.saleid == Sale.saleid).\
    #         join(Product, Product.productid == OrderItem.productid).\
    #         join(Category, Category.categoryid == Product.categoryid).\
    #         filter(
    #             Sale.salesdate.between(start_date, end_date),
    #             extract('year', Sale.salesdate) == year,
    #             Category.categoryid == categoryid
    #         ).\
    #         scalar() or 0
    #     self.db_manager.close_session(self.session)
    #     return yearly_revenue
    
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
        



    def calculate_revenue_daily_by_category(self, start_date, end_date, categoryid):

        # Retrieve sales data between start_date and end_date
        sales_data = self.session.query(Sale.salesdate, Sale.totalsaleamount) \
            .join(OrderItem, OrderItem.saleid == Sale.saleid) \
            .join(Product, Product.productid == OrderItem.productid) \
            .join(Category, Category.categoryid == Product.categoryid) \
            .filter(Sale.salesdate.between(start_date, end_date), Category.categoryid == categoryid) \
            .all()

        # Create a dictionary to store sales data by date
        sales_by_date = defaultdict(int)
        
        # Accumulate the sales amounts for each date
        # Accumulate the sales amounts for each date
        for date, amount in sales_data:
            sales_by_date[date.strftime('%Y-%m-%d')] += amount

        # Create a date array between start_date and end_date
        date_array = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

        # Map the results to the date array along with start and end dates for each day
        daily_revenue = [(date.strftime('%Y-%m-%d'), date, date, sales_by_date.get(date.strftime('%Y-%m-%d'), 0)) for date in date_array]

        self.db_manager.close_session(self.session)

        return daily_revenue
    
    def calculate_revenue_monthly_by_category(self, start_date, end_date, categoryid):
        # Create a dictionary to store sales data by month
        sales_by_month = defaultdict(int)

        # Retrieve sales data between start_date and end_date
        sales_data = self.session.query(Sale.salesdate, Sale.totalsaleamount) \
            .join(OrderItem, OrderItem.saleid == Sale.saleid) \
            .join(Product, Product.productid == OrderItem.productid) \
            .join(Category, Category.categoryid == Product.categoryid) \
            .filter(Sale.salesdate.between(start_date, end_date), Category.categoryid == categoryid) \
            .all()

        for date, amount in sales_data:
                # Use the month and year as the key
            key = (date.strftime('%Y-%m'))
            sales_by_month[key] += amount

        # Generate a list of months between start_date and end_date
        monthly_revenue = []
        current_date = start_date.replace(day=1)
        while current_date <= end_date:
            month = current_date.strftime('%Y-%m')
            next_month_date = current_date + relativedelta(months=1) - timedelta(days=1)
            monthly_revenue.append((month, current_date, next_month_date, sales_by_month.get(month, 0)))
            current_date += relativedelta(months=1)

        self.db_manager.close_session(self.session)

        return monthly_revenue


    
    def calculate_revenue_weekly_by_category(self, start_date, end_date, categoryid):
        # Retrieve sales data between start_date and end_date
        sales_data = self.session.query(Sale.salesdate, Sale.totalsaleamount) \
            .join(OrderItem, OrderItem.saleid == Sale.saleid) \
            .join(Product, Product.productid == OrderItem.productid) \
            .join(Category, Category.categoryid == Product.categoryid) \
            .filter(Sale.salesdate.between(start_date, end_date), Category.categoryid == categoryid) \
            .all()

        # Create a dictionary to store sales data by week
        sales_by_week = defaultdict(int)

        for date, amount in sales_data:
                # Calculate the week number for the given date
            week_number = (date - start_date).days // 7

            # Use the week number as the key
            sales_by_week[week_number] += amount

        # Create a list of week numbers between start_date and end_date
        week_numbers = range((end_date - start_date).days // 7 + 1)

        # Calculate start and end dates for each week
        weekly_revenue = [(start_date + timedelta(weeks=week),
                           start_date + timedelta(weeks=week), 
                            start_date + timedelta(weeks=week, days=6), 
                            sales_by_week.get(week, 0)) 
                            for week in week_numbers]

        self.db_manager.close_session(self.session)

        return weekly_revenue
    
        
        
    def calculate_revenue_yearly_by_category(self, start_date, end_date, categoryid):
        # Create a dictionary to store sales data by year
        sales_by_year = defaultdict(int)

        # Retrieve sales data between start_date and end_date
        sales_data = self.session.query(Sale.salesdate, Sale.totalsaleamount) \
            .join(OrderItem, OrderItem.saleid == Sale.saleid) \
            .join(Product, Product.productid == OrderItem.productid) \
            .join(Category, Category.categoryid == Product.categoryid) \
            .filter(Sale.salesdate.between(start_date, end_date), Category.categoryid == categoryid) \
            .all()

        # Accumulate the sales amounts for each year
        for date, amount in sales_data:
            # Use the year as the key
            key = date.year
            sales_by_year[key] += amount

        # Generate a list of years between start_date and end_date
        yearly_revenue = []
        current_year = start_date.year
        while current_year <= end_date.year:
            year_start_date = start_date.replace(year=current_year, month=1, day=1)
            year_end_date = start_date.replace(year=current_year, month=12, day=31)
            yearly_revenue.append((current_year, year_start_date, year_end_date, sales_by_year.get(current_year, 0)))
            current_year += 1

        self.db_manager.close_session(self.session)

        return yearly_revenue