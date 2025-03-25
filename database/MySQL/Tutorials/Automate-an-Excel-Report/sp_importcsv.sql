CREATE OR ALTER PROCEDURE ImportCSV
AS
BEGIN
    DELETE FROM dbo.cust_orders;

    BULK INSERT dbo.cust_orders
	FROM 'C:\Users\Indre\Downloads\projects_run\DevDocs\database\MySQL\Tutorials\Automate-an-Excel-Report\cust_orders.csv'
	WITH
	(
	  FIRSTROW=2,
	  FIELDTERMINATOR =',',
	  ROWTERMINATOR = '0x0a'
	);
END;

EXECUTE ImportCSV