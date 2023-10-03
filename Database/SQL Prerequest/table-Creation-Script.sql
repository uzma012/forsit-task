CREATE TABLE Admin (
  AdminID     bigint IDENTITY NOT NULL, 
  Name        varchar(30) NOT NULL, 
  Phone int NOT NULL, 
  Email       varchar(50) NOT NULL, 
  PRIMARY KEY (AdminID));
CREATE UNIQUE INDEX Admin_AdminID 
  ON Admin (AdminID);


  CREATE TABLE Customer (
  CustomerId bigint IDENTITY NOT NULL, 
  FirstName  varchar(30) NOT NULL, 
  LastName   varchar(30) NOT NULL, 
  Email      varchar(50) NOT NULL, 
  Phone      int NOT NULL, 
  Address    varchar(100) NOT NULL, 
  CONSTRAINT CustomerId 
    PRIMARY KEY CLUSTERED (CustomerId));
CREATE UNIQUE INDEX Customer_CustomerId 
  ON Customer (CustomerId);



CREATE TABLE Category (
  CategoryId   bigint IDENTITY NOT NULL, 
  CategoryName nvarchar(50) NOT NULL, 
  AdminID      bigint NOT NULL, 
  PRIMARY KEY (CategoryId));
CREATE UNIQUE INDEX Category_CategoryId 
  ON Category (CategoryId);
ALTER TABLE Category ADD CONSTRAINT FKCategory296749 FOREIGN KEY (AdminID) REFERENCES Admin (AdminID);

 CREATE TABLE [Order] (
  OrderID     int IDENTITY NOT NULL, 
  OrderDate   date NOT NULL, 
  TotalAmount decimal(19, 0) NOT NULL, 
  CustomerId  bigint NOT NULL, 
  PRIMARY KEY (OrderID));
CREATE UNIQUE INDEX Order_OrderID 
  ON [Order] (OrderID);
ALTER TABLE [Order] ADD CONSTRAINT FKOrder835073 FOREIGN KEY (CustomerId) REFERENCES Customer (CustomerId);


CREATE TABLE Revenue (
  RevenueID    int IDENTITY NOT NULL, 
  Amount       decimal(19, 0) NOT NULL, 
  [Date]       date NOT NULL, 
  OrderID int NOT NULL, 
  PRIMARY KEY (RevenueID));
CREATE UNIQUE INDEX Revenue_RevenueID 
  ON Revenue (RevenueID);
ALTER TABLE Revenue ADD CONSTRAINT FKRevenue230767 FOREIGN KEY (OrderID) REFERENCES [Order] (OrderID);



CREATE TABLE Product (
  ProductID       bigint IDENTITY NOT NULL, 
  Description     varchar(255) NULL, 
  ProductName     varchar(255) NOT NULL, 
  Price           decimal(19, 0) NOT NULL, 
  QuantityInStock int NOT NULL, 
  CategoryId      bigint NOT NULL, 
  AdminID         bigint NOT NULL, 
  PRIMARY KEY (ProductID));
CREATE UNIQUE INDEX Product_ProductID 
  ON Product (ProductID);
ALTER TABLE Product ADD CONSTRAINT FKProduct608700 FOREIGN KEY (CategoryId) REFERENCES Category (CategoryId);
ALTER TABLE Product ADD CONSTRAINT FKProduct649616 FOREIGN KEY (AdminID) REFERENCES Admin (AdminID);

CREATE TABLE InventoryTransaction (
  TransactionID   bigint IDENTITY NOT NULL, 
  TransactionDate date NOT NULL, 
  TransactionType nvarchar(50) NOT NULL, 
  QuantityChanged int NOT NULL, 
  ProductID       bigint NOT NULL, 
  AdminID         bigint NOT NULL, 
  PRIMARY KEY (TransactionID));
CREATE UNIQUE INDEX InventoryTransaction_TransactionID 
  ON InventoryTransaction (TransactionID);
ALTER TABLE InventoryTransaction ADD CONSTRAINT FKInventoryT847521 FOREIGN KEY (ProductID) REFERENCES Product (ProductID);
ALTER TABLE InventoryTransaction ADD CONSTRAINT FKInventoryT808482 FOREIGN KEY (AdminID) REFERENCES Admin (AdminID);


CREATE TABLE Sale (
  SaleID          int IDENTITY NOT NULL, 
  SalesDate       date NOT NULL, 
  TotalSaleAmount decimal(19, 0) NOT NULL, 
  CustomerId      bigint NOT NULL, 
  PRIMARY KEY (SaleID));
CREATE UNIQUE INDEX Sales_SaleID 
  ON Sale (SaleID);
ALTER TABLE Sales ADD CONSTRAINT FKSales30403 FOREIGN KEY (CustomerId) REFERENCES Customer (CustomerId);

CREATE TABLE OrderItem (
  OrderItemID int IDENTITY NOT NULL, 
  Quantity    int NOT NULL, 
  Subtotal    decimal(19, 0) NOT NULL, 
  ProductID   bigint NOT NULL, 
  OrderID     int NOT NULL, 
  SaleID      int NOT NULL, 
  PRIMARY KEY (OrderItemID));
CREATE UNIQUE INDEX OrderItem_OrderItemID 
  ON OrderItem (OrderItemID);
ALTER TABLE OrderItem ADD CONSTRAINT FKOrderItem557764 FOREIGN KEY (ProductID) REFERENCES Product (ProductID);
ALTER TABLE OrderItem ADD CONSTRAINT FKOrderItem358842 FOREIGN KEY (OrderID) REFERENCES [Order] (OrderID);
ALTER TABLE OrderItem ADD CONSTRAINT FKOrderItem981014 FOREIGN KEY (SaleID) REFERENCES Sales (SaleID);


CREATE TABLE InventoryHistory (
  transactionId   bigint IDENTITY NOT NULL, 
  transactionDate date NOT NULL, 
  QuantityChanged int NOT NULL, 
  TransactionType nvarchar(50) NOT NULL, 
  ProductID       bigint NOT NULL, 
  PRIMARY KEY (transactionId));
CREATE INDEX InventoryHistory_transactionId 
  ON InventoryHistory (transactionId);
ALTER TABLE InventoryHistory ADD CONSTRAINT FKInventoryH833871 FOREIGN KEY (ProductID) REFERENCES Product (ProductID);
