# Database utility functions
# utils/db_utils.py

import pyodbc
from config import AzureSQLConfig
from datetime import datetime, timezone



# Connection Management
def getDbConnection():
    connection = pyodbc.connect(AzureSQLConfig.connectionString)
    return connection

# User Management
def createUser(name, email, dicePassword, hashedPassword):
    connection = getDbConnection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (email, name, hashed_password, last_view, dice_password) VALUES (?, ?, ?, 940704000, ?)",
            (email, name, hashedPassword, dicePassword)
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
            user = {'email': row[0], 'name': row[1], 'hashed_password': row[2], 'last_view': row[3]}
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

def updateLastView(email, newLastView):
    connection = getDbConnection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "UPDATE users SET last_view = ? WHERE email = ?",
            (newLastView, email)
        )
        connection.commit()
    except pyodbc.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

def getUserLastView(email):
    connection = getDbConnection()
    cursor = connection.cursor()
    lastView = None
    try:
        cursor.execute("SELECT last_view FROM users WHERE email = ?", (email,))
        result = cursor.fetchone()
        if result:
            lastView = result[0]
    except pyodbc.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()
    return lastView

# Job Management
def loadJobsTill(lastView):
    connection = getDbConnection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
                SELECT TOP 20 id, title, description, company, dateUpdated
                FROM allData
                WHERE dateUpdated > ?
                ORDER BY dateUpdated ASC
            """,
            (lastView,)
        )
        rows = cursor.fetchall()
        jobQueue = [{'id': row[0], 'title': row[1], 'description': row[2], 'company': row[3], 'timeOfArrival': str(row[4])} for row in rows]
    except pyodbc.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()
    return jobQueue

def addToApplyQueue(jobID, selectedResume, email):
    connection = getDbConnection()
    cursor = connection.cursor()
    try:
        timestamp = int(datetime.now(timezone.utc).timestamp())
        cursor.execute(
            """
                INSERT INTO applyQueue (id, timeOfArrival, selectedResume, email)
                SELECT ?, ?, ?, ?
                WHERE NOT EXISTS (
                    SELECT 1 FROM applyQueue WHERE id = ?
                );
            """,
            (jobID, timestamp, selectedResume, email, jobID)
        )
        if cursor.rowcount != 1:
            print(f"JobID {jobID} already exists in apply queue. No duplicate added.")
        else:
            print(f"Added JobID {jobID} to apply queue")
        connection.commit()
    except pyodbc.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

# Resume Management
def addResumeToDatabase(resumeID, resumeName, email):
    connection = getDbConnection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO resumeList (resumeId, resumeName, email) VALUES (?, ?, ?)",
            (resumeID, resumeName, email)
        )
        connection.commit()
    except pyodbc.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

def deleteResumeFromDatabase(resumeId):
    connection = getDbConnection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "DELETE FROM resumeList WHERE resumeId = ?",
            (resumeId,)
        )
        connection.commit()
    except pyodbc.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

def getUsersResumes(email):
    connection = getDbConnection()
    cursor = connection.cursor()
    resumeData = {}
    try:
        # cursor.execute("SELECT * FROM resumeList")
        cursor.execute(
            "SELECT * FROM resumeList WHERE email = ?", 
            (email,)
        )
        rows = cursor.fetchall()
        resumeData = {row[0]: row[1] for row in rows}
    except pyodbc.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()
    print(resumeData)
    return resumeData
