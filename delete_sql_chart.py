import pyodbc
from pylogix import PLC

connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                           'Server= AYUSHP-DELL\\SQLEXPRESS03;'
                           'Trusted_Connection=yes;')

if connection:
    print("Connected Successfully")
else:
    print("Failed to connect")

cursor = connection.cursor()

def delete_all_rows_X_Chart(cursor):
    table_name = 'Control_chart.dbo.[X_CHART]'
    SQLCommand = f"DELETE FROM {table_name}"
    cursor.execute(SQLCommand)
    connection.commit()  # Commit changes to the database

def delete_all_rows_R_Chart(cursor):
    table_name = 'Control_chart.dbo.[R_CHART]'
    SQLCommand = f"DELETE FROM {table_name}"
    cursor.execute(SQLCommand)
    connection.commit()  # Commit changes to the database

def delete_all_rows_Histogram(cursor):
    table_name = 'Control_chart.dbo.[Histogram]'
    SQLCommand = f"DELETE FROM {table_name}"
    cursor.execute(SQLCommand)
    connection.commit()

def delete_all_rows_SOLO_Chart(cursor):
    table_name = 'Control_chart.dbo.[SOLO_CHART]'
    SQLCommand = f"DELETE FROM {table_name}"
    cursor.execute(SQLCommand)
    connection.commit()

delete_all_rows_R_Chart(cursor)
delete_all_rows_X_Chart(cursor)
delete_all_rows_Histogram(cursor)
delete_all_rows_SOLO_Chart(cursor)