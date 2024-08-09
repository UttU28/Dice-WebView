# Database utility functions
# utils/db_utils.py

import pyodbc
from config import AzureSQLConfig

def getDbConnection():
    connection = pyodbc.connect(AzureSQLConfig.connectionString)
    return connection

def createUser(name, email, hashedPassword):
    connection = getDbConnection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (email, name, hashed_password, lastVisit) VALUES (?, ?, ?, 940704000)",
            (email, name, hashedPassword)
        )
        connection.commit()
    except pyodbc.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

def loadJobsTill(lastView):
    connection = getDbConnection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
                SELECT TOP 20 id, title, description, company, dateUpdated
                FROM allData
                WHERE dateUpdated > ?
                ORDER BY dateUpdated DESC
            """,
            (lastView)
        )
        connection.commit()
    except pyodbc.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

def getUserByEmail(email):
    connection = getDbConnection()
    cursor = connection.cursor()
    user = None
    try:
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        if row:
            user = {'email': row[0], 'name': row[1], 'hashed_password': row[2], 'lastView': row[3]}
    except pyodbc.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()
    return user

def updatePassword(email, hashedPassword):
    connection = getDbConnection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "UPDATE users SET hashed_password = ? WHERE email = ?",
            (hashedPassword, email)
        )
        connection.commit()
    except pyodbc.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

def updateLastView(email, hashedPassword):
    connection = getDbConnection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "UPDATE users SET hashed_password = ? WHERE email = ?",
            (hashedPassword, email)
        )
        connection.commit()
    except pyodbc.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()
