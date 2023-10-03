# forsit-task
In this project the inventory managment system is build. Followings are the folder with purpose explained breifly.

# Database
In this folder all the database requirement files are placed. 
 * Database ERD: This folder contain the ERD of e-commerce Inventory managment system. ERD is based on assumptions. The file named "Explaination of ERD" contains the breif discription of the purpose and relationship between each tables. Other files are of database ERD open in "visual paradim"
* SQL Prerequest: This folder contains the files related to creation and data insertion of db tables.

# Main Project 
This folder contains the apis and all the other files needed during project.
 * DTOs : This folder contains all the request and response models.
 * Models : This folder contains all the DB models in python. 
 * InventoryService: This file contains the implementation of inventory related apis.
 * ProductService : This file contains the implementation of product related apis.
 * SalesService : This file contains the implementation of sales and revenue related apis.
 * Controller : This is the main file that contains all the apis.
 * requirement : This file contains all the requirements to run the code.

# Inventory.postman_collection.json
This file contains the requests endpoints and bodies. 
 * Revenue APIs:
        Get revenue by date and category_id
        - Request endpoint : \revenue
        - Method : Post
        - period parameter will be:
                    "d" = daily data
                    "w" = weekly
                    "m" = monthly
                    "y" = yearly 
        - request body :  send both dates and category_id or send category_id or send date.
                        {
                            "start_date":"2023-09-25",
                            "end_date":"2024-09-01",
                            "period":"w",
                            "category_id":1 //optional
                        }
 * Sales APIs: 
        get dales data by filters
        - Request endpoint : \sales_data
        - Method : Post
        - request body :   {
                                "start_date": "2023-09-25",
                                "end_date": "2024-09-01",
                                "category_id": 2,
                                "product_id": 2
                            }
        - request body by dates:
                              {
                                  "start_date":"2023-09-25",
                                  "end_date":"2024-09-01"
                              }
        - request body by category id:
                              {
                                  "category_id":2
                              }
        - request body by product id : 
                                {
                                    "product_id":2
                                }
        - request body by category id  and date:                         
                               {
                                   "start_date":"2023-09-25",
                                   "end_date":"2024-09-01",
                                   "category_id":2,
                               }
        - request body by product id  and date:  
                               {
                                   "start_date":"2023-09-25",
                                   "end_date":"2024-09-01",
                                   "product_id":2
                               }
 * Inventory APIs:
        Get inventory items
        -request : \inventory
        -method : Get
        -optional parameter: threshold=10 (default 10)

        Update inventory
        -request : \inventory
        -method : Post
        -body:
                    {
                        "product_id":2,
                        "quantity_changed":10,
                        "transaction_type":"Purchase",
                        "adminId":1
                    }
 * Product APIs:
        Add new product or update existing product based on name.
        -request : \product
        -method : Post
        -body:
                {
                    "product_name": "socks",
                    "description": "nike",
                    "price": 20,
                    "quantity_in_stock": 100,
                    "transaction_type":"Purchase",
                    "admin_id":2,
                    "categoryId":2
                }
 
# run instructions
To run code follow the steps:
 * Create db and run the script for table creation.
 * Insert data in tables by running the table insertion script.
 * replace database_url = 'mssql+pyodbc://localhost/inventory?driver=SQL+Server+Native+Client+11.0' this in Controller.py with your own database_url.
 * run the code by unvicorn Controller:app --reload
 * open the postman or anyother related software and use the above request to call apis
