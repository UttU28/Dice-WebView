# Configuration file for Flask and Azure SQL connection
# config.py

import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')  # For session management, CSRF protection, etc.

class AzureSQLConfig(Config):
    databaseServer = os.getenv('databaseServer')
    databaseName = os.getenv('databaseName')
    databaseUsername = os.getenv('databaseUsername')
    databasePassword = os.getenv('databasePassword')
    connectionString = (
        f"Driver={{ODBC Driver 17 for SQL Server}};"
        f"Server=tcp:{databaseServer},1433;"
        f"Database={databaseName};"
        f"Uid={databaseUsername};"
        f"Pwd={databasePassword};"
        f"Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    )

class AzureBLOBConfig(Config):
    AZURE_CONNECTION_STRING = os.getenv('blobConnectionString')
    CONTAINER_NAME = 'resume-data'



# databaseServer = 'dice-sql.database.windows.net'
# databaseName = 'dice_sql_database'
# databaseUsername = 'iAmRoot'
# databasePassword = 'Qwerty@213'
# connectionString = f'Driver={{ODBC Driver 17 for SQL Server}};Server=tcp:{databaseServer},1433;Database={databaseName};Uid={databaseUsername};Pwd={databasePassword};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'