import os
import pypyodbc as odbc

databaseServer = 'dice-sql.database.windows.net'
databaseName = 'dice_sql_database'
databaseUsername = 'iAmRoot'
databasePassword = 'Qwerty@213'

# REPLACE THIS BIJSBKJFNKJBSNK JFBN:SKJFNI A: HFUNLIAUKGDKAGYDKHYAGVKHGAVKGHAKHGV
# connectionString = f'Driver={{ODBC Driver 17 for SQL Server}};Server=tcp:{server},1433;Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=5;'
connectionString = f'Driver={{ODBC Driver 17 for SQL Server}};Server=tcp:{databaseServer},1433;Database={databaseName};Uid={databaseUsername};Pwd={databasePassword};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

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