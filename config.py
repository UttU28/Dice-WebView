# Configuration file for Flask and Azure SQL connection
# config.py

import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')  # For session management, CSRF protection, etc.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class AzureSQLConfig(Config):
    databaseServer = 'dice-sql.database.windows.net'
    databaseName = 'dice_sql_database'
    databaseUsername = 'iAmRoot'
    databasePassword = 'Qwerty@213'
    connectionString = (
        f"Driver={{ODBC Driver 17 for SQL Server}};"
        f"Server=tcp:{databaseServer},1433;"
        f"Database={databaseName};"
        f"Uid={databaseUsername};"
        f"Pwd={databasePassword};"
        f"Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    )
