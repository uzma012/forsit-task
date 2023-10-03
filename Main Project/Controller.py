from sqlalchemy.ext.declarative import declarative_base
from Models.DBContext import DatabaseManager
from fastapi import FastAPI
import uvicorn
from typing import List, Optional
from datetime import datetime, timedelta
from typing import List
from SalesService import SalesServices
from DTOs.SalesResponse import SalesResponse
from DTOs.SalesRequest import SalesRequest
from DTOs.RevenueRequest import RevenueRequest
from DTOs.RevenueResponse import RevenueResponse
from InventoryService import InventoryServices
from DTOs.InventoryResponse import InventoryResponse
from DTOs.InventoryUpdateRequest import InventoryUpdateRequest
from DTOs.RegisterProductRequest import RegisterProductRequest

Base = declarative_base()
app = FastAPI()

database_url = 'mssql+pyodbc://localhost/inventory?driver=SQL+Server+Native+Client+11.0'
db_manager = DatabaseManager(database_url)
db_manager.create_tables()
session = db_manager.get_session()
Inventory_service=InventoryServices(db_manager,session)
sales_service=SalesServices(db_manager,session)
date_format = '%Y-%m-%d'

# Convert the string to a datetime object
@app.post("/sales_data", response_model=List[SalesResponse])
async def get_sales_data(sales_data_request:SalesRequest ):
    if(sales_data_request.start_date  and sales_data_request.end_date):
        start_date=datetime.strptime(sales_data_request.start_date, date_format).date()
        end_date=datetime.strptime(sales_data_request.end_date, date_format).date()
        sales_by_product_and_category = sales_service.get_sales_by_criteria(start_date, end_date,sales_data_request.product_id,sales_data_request.category_id)
        return sales_by_product_and_category
    else:
        
        if sales_data_request.product_id is None and sales_data_request.category_id is not None:
            sales_by_product_and_category = sales_service.get_sales_by_category(sales_data_request.category_id)
            return sales_by_product_and_category
        
        elif sales_data_request.product_id is not None and sales_data_request.category_id is None:
            sales_by_product_and_category = sales_service.get_sales_by_product(sales_data_request.product_id)
            return sales_by_product_and_category
        

@app.post("/revenue", response_model=List[RevenueResponse])
async def get_sales_data(revenue_request:RevenueRequest ):
    if(revenue_request.category_id is None):
        start_date=datetime.strptime(revenue_request.start_date, date_format).date()
        end_date=datetime.strptime(revenue_request.end_date, date_format).date()
        revenu_reponse = sales_service.compare_revenue_across_periods_and_categories(start_date, end_date)
        return revenu_reponse
    else:
        start_date=datetime.strptime(revenue_request.start_date, date_format).date()
        end_date=datetime.strptime(revenue_request.end_date, date_format).date()
        revenu_reponse = sales_service.compare_revenue_across_periods_and_categories(start_date, end_date,revenue_request.category_id)
        return revenu_reponse
        

@app.get("/inventory", response_model=List[InventoryResponse])
async def get_sales_data(threshold: Optional[int] = 0):
    reponse = Inventory_service.view_inventory_status(threshold)
    return reponse
        

@app.post("/inventory", response_model=bool)
async def get_sales_data(inventory_update_request: InventoryUpdateRequest):
    reponse = Inventory_service.update_inventory(inventory_update_request.product_id,
                                                 inventory_update_request.quantity_changed,
                                                 inventory_update_request.transaction_type,
                                                 inventory_update_request.adminId)
    return reponse

@app.post("/product", response_model=bool)
async def get_sales_data(register_new_product: RegisterProductRequest):
    reponse = Inventory_service.register_new_product(register_new_product.product_name,
                                                 register_new_product.description,
                                                 register_new_product.price,
                                                 register_new_product.quantity_in_stock,
                                                 register_new_product.transaction_type,
                                                 register_new_product.admin_id)
    return reponse


# # Calculate daily revenue for a specific date
# date = datetime(2023, 9, 30)
# daily_revenue =sales_service.calculate_revenue_daily(date)
# print(f"Daily Revenue for {date}: {daily_revenue}")

# # Calculate weekly revenue for a specific week (start date)
# start_date = datetime(2023, 9, 25)  # Assuming Monday of the desired week
# weekly_revenue = sales_service.calculate_revenue_weekly(start_date)
# print(f"Weekly Revenue for the week starting from {start_date}: {weekly_revenue}")

# # Calculate monthly revenue for a specific year and month
# year = 2023
# month = 9
# monthly_revenue = sales_service.calculate_revenue_monthly(year, month)
# print(f"Monthly Revenue for {month}/{year}: {monthly_revenue}")

# # Calculate annual revenue for a specific year
# year = 2023
# annual_revenue = sales_service.calculate_revenue_annually(year)
# print(f"Annual Revenue for {year}: {annual_revenue}")

# start_date = datetime(2023, 9, 1)
# end_date = datetime(2023, 10, 30)
# sales_within_date_range = sales_service.get_sales_by_date_range(start_date, end_date)

# for sale in sales_within_date_range:
#     print(f"Sale ID: {sale.saleid}, Date: {sale.salesdate}, Total Sale Amount: {sale.totalsaleamount}")

# customer_id = 2  # Assuming customer ID 1
# sales_for_customer = sales_service.get_sales_by_customer(customer_id)

# for sale in sales_for_customer:
#     print(f"Sale ID: {sale.saleid}, Date: {sale.salesdate}, Total Sale Amount: {sale.totalsaleamount}")
    

# total_sales_amount = sales_service.calculate_total_sales_amount(sales_within_date_range)
# print(f"Total Sales Amount: {total_sales_amount}")


# start_date = datetime(2023, 9, 1)
# end_date = datetime(2023, 10, 30)
# period = 'daily'  # Choose from: daily, weekly, monthly, yearly
# categories = [1, 2]  # Replace with your actual category IDs

# # # Compare revenue across periods and categories
# comparison_results = sales_service.compare_revenue_across_periods_and_categories(start_date, end_date,1)

# # Display the comparison results
# for category_data in comparison_results:
#     print(f"Category: {category_data['categoryname']}")
#     print("Revenue by Period:")
#     for period, revenue in category_data['revenue_by_period'].items():
#         print(f"  {period.capitalize()}: {revenue}")
#     print()


# product_id = 1  # Replace with the desired product ID
# sales_by_product = sales_service.get_sales_by_criteria(start_date, end_date, product_id=product_id)

# # Fetch sales data within the date range for a specific category (optional)
# category_id = 1  # Replace with the desired category ID
# sales_by_category = sales_service.get_sales_by_criteria(start_date, end_date, category_id=category_id)

# # Fetch sales data within the date range for a specific product and category (optional)
# product_id = 1  # Replace with the desired product ID
# category_id = 2  # Replace with the desired category ID
# sales_by_product_and_category = sales_service.get_sales_by_criteria(start_date, end_date)

# # Print the sales data (customize the output based on your Sale model structure)
# for sale in sales_by_product:
#     print(f"Sale Date: {sale.salesdate}, Total Sale Amount: {sale.totalsaleamount}")

# for sale in sales_by_category:
#     print(f"Sale Date: {sale.salesdate}, Total Sale Amount: {sale.totalsaleamount}")

# for sale in sales_by_product_and_category:
#     print(f"Sale Date: {sale.salesdate}, Total Sale Amount: {sale.totalsaleamount}")
    


# low_stock_threshold = 10
# Inventory_service.view_inventory_status(low_stock_threshold)

# product_id = 1
# quantity_changed = 5
# transaction_type = 'Purchase'

# # Update inventory and track the change
# Inventory_service.update_inventory(product_id, quantity_changed, transaction_type)