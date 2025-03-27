CREATE TABLE cust_orders (
  cust_id INTEGER,
  order_date DATE,
  order_amount INTEGER
);

BULK INSERT dbo.cust_orders
FROM 'C:\Users\Indre\Downloads\projects_run\DevDocs\database\MySQL\Tutorials\Automate-an-Excel-Report\cust_orders.csv'
WITH
(
  FIRSTROW=2,
  FIELDTERMINATOR =',',
  ROWTERMINATOR = '0x0a'
);

SELECT * FROM dbo.cust_orders
