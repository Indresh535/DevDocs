# Configuration file for URL, browser type, etc.
import urllib
import os

#aws_access_key = os.getenv("AWS_ACCESS_KEY")
#aws_secret_key = os.getenv("AWS_SECRET_KEY")


# aws_access_key = 'AKIAWVBXPP3ID4NT6CUP'
# aws_secret_key = 'yjMGJ6scevKg82eiZicDJw55ajhpBBOdQh7YC9i'
password = urllib.parse.quote_plus('hh')
# connection_string = f'mssql+pyodbc://gfuser:{password}@stagedb/CustomerProfile_CC?driver=ODBC+Driver+17+for+SQL+Server'
# Connection string for SQLAlchemy
# connection_string = 'mssql+pyodbc://user:password@server/dbName?driver=ODBC+Driver+17+for+SQL+Server'
connection_string = 'mssql+pyodbc://sa:1234@DELL/testdb?driver=ODBC+Driver+17+for+SQL+Server'