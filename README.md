
# E-commerce Inventory Management System

This project is an E-commerce Inventory Management System designed to efficiently manage products, sales, revenue, and inventory. Below are the folders and components explained briefly.

## Database

This folder contains all the database-related files.

- **Database ERD**: This folder contains the Entity-Relationship Diagram (ERD) of the E-commerce Inventory Management System. The ERD represents the database structure based on assumptions. Refer to the "Explaination of ERD" file for a brief description of the table purposes and relationships. Other files in this folder are ERD diagrams opened in "Visual Paradigm."

- **SQL Prerequisites**: This folder contains files related to creating database tables and inserting initial data.

## Main Project

This folder contains the core components of the project.

- **DTOs**: This folder holds all the Data Transfer Objects (DTOs), including request and response models.

- **Models**: The Models folder contains Python classes representing the database tables.

- **InventoryService**: This file contains the implementation of inventory-related APIs.

- **ProductService**: The ProductService file contains the implementation of APIs related to managing products.

- **SalesService**: In SalesService, you'll find the implementation of APIs related to sales and revenue.

- **Controller**: The Controller file is the main entry point for all APIs. It contains the routing logic.

- **requirement**: This file lists all the project dependencies required to run the code.

## Inventory.postman_collection.json

This file includes a Postman collection with pre-defined requests, endpoints, and request bodies for testing the APIs.

### Revenue APIs

- **Get Revenue by Date and Category**
  - Request endpoint: `/revenue`
  - Method: POST
  - Parameters:
    - `period`: Specify the period as "d" (daily), "w" (weekly), "m" (monthly), or "y" (yearly).
  - Request body options:
    - Provide both `start_date` and `end_date` along with an optional `category_id`.
    - Provide only `category_id`.
    - Provide only `start_date` and `end_date`.

### Sales APIs

- **Get Sales Data by Filters**
  - Request endpoint: `/sales_data`
  - Method: POST
  - Request body options:
    - Filter by date range: Provide `start_date` and `end_date`.
    - Filter by `category_id` or `product_id`.
    - Combine date range with `category_id` or `product_id`.

### Inventory APIs

- **Get Inventory Items**
  - Request: `/inventory`
  - Method: GET
  - Optional parameter: `threshold` (default is 10)

- **Update Inventory**
  - Request: `/inventory`
  - Method: POST
  - Request body: Specify `product_id`, `quantity_changed`, `transaction_type`, and `admin_id`.

### Product APIs

- **Add or Update Product**
  - Request: `/product`
  - Method: POST
  - Request body: Provide product details including `product_name`, `description`, `price`, `quantity_in_stock`, `transaction_type`, `admin_id`, and `categoryId`.

## Run Instructions

To run the project, follow these steps:

1. Create the database and run the script for table creation.

2. Insert data into the tables by executing the table insertion script.

3. Replace `database_url` in `Controller.py` with your own database URL.

4. Run the code using Gunicorn: `uvicorn Controller:app --reload`.

5. Use Postman or similar software to call the APIs using the provided requests in the Postman collection.

Feel free to reach out if you have any questions or need further assistance!
