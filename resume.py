import os
import pypyodbc as odbc
from credential import *

server = 'dice-sql.database.windows.net'
database = 'dice_sql_database'

connectionString = f'Driver={{ODBC Driver 18 for SQL Server}};Server=tcp:{server},1433;Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'


def addResumeToDatabase(directory):
    conn = odbc.connect(connectionString)
    cursor = conn.cursor()

    all_resumes = [filename for filename in os.listdir(directory) if filename.endswith('.pdf')]

    for resume_name in all_resumes:
        query = "INSERT INTO resumeList (resumeName) VALUES (?)"
        cursor.execute(query, (resume_name,))
        conn.commit()

    cursor.close()
    conn.close()

directory = 'allResume'
addResumeToDatabase(directory)

print("Resumes added to database successfully.")