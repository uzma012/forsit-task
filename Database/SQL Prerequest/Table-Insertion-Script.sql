-- Insert sample data for Admin
INSERT INTO Admin (Name, Email, Phone)
VALUES 
  ('Admin 1', 'admin1@example.com', '123456789'),
  ('Admin 2', 'admin2@example.com', '987654321');

-- Insert sample data for Category
INSERT INTO Category (CategoryName, AdminId)
VALUES 
  ('Electronics', 1),
  ('Clothing', 2);

-- Insert sample data for Product
INSERT INTO Product (ProductName, Description, Price, QuantityInStock, CategoryID, AdminId)
VALUES 
  ('Laptop', 'High-performance laptop', 1000.00, 50, 1, 1),
  ('T-Shirt', 'Cotton T-Shirt', 20.00, 100, 2, 2);

-- Insert sample data for Customer
INSERT INTO Customer (FirstName, LastName, Email, Phone, Address)
VALUES 
  ('John', 'Doe', 'john.doe@example.com', '111111111', '1234 Elm St'),
  ('Jane', 'Smith', 'jane.smith@example.com', '222222222', '5678 Oak St');

-- Insert sample data for Order
INSERT INTO [Order] (OrderDate, TotalAmount, CustomerID)
VALUES 
  ('2023-09-30', 1000.00, 1),
  ('2023-10-01', 60.00, 2);

-- Insert sample data for Sale
INSERT INTO Sale (SalesDate, TotalSaleAmount, CustomerID)
VALUES 
  ('2023-09-30', 2000.00, 1),
  ('2023-10-01', 60.00, 2);

-- Insert sample data for OrderItem
INSERT INTO OrderItem (Quantity, Subtotal, ProductID, OrderID, SaleId)
VALUES 
  (2, 2000.00, 1, 1, 1),
  (3, 60.00, 2, 2, 2);

-- Insert sample data for InventoryTransaction
INSERT INTO InventoryTransaction (TransactionDate, TransactionType, QuantityChanged, ProductID, AdminID)
VALUES 
  ('2023-09-30', 'Purchase', 20, 1, 1),
  ('2023-10-01', 'Sale', -10, 2, 2);

-- Insert sample data for Revenue
INSERT INTO Revenue (Date, Amount, OrderID)
VALUES 
  ('2023-09-30', 2000.00, 1),
  ('2023-10-01', 60.00, 2);



  --delete from Product
  --delete from Revenue
  --delete from sale
  --delete from InventoryTransaction
  --delete from dbo.[Order]
  --delete from OrderItem
  --delete from Category
  --delete from Customer
  --delete from Admin


--DBCC CHECKIDENT ('Admin', RESEED, 0);
--GO
--DBCC CHECKIDENT ('[Category]', RESEED, 0);
--GO
--DBCC CHECKIDENT ('[Customer]', RESEED, 0);
--GO
--DBCC CHECKIDENT ('[InventoryTransaction]', RESEED, 0);
--GO
--DBCC CHECKIDENT ('[Order]', RESEED, 0);
--GO
--DBCC CHECKIDENT ('[OrderItem]', RESEED, 0);
--GO
--DBCC CHECKIDENT ('[Product]', RESEED, 0);
--GO
--DBCC CHECKIDENT ('[Sale]', RESEED, 0);
--GO
--DBCC CHECKIDENT ('[Revenue]', RESEED, 0);
--GO