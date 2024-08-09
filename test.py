import pypyodbc as odbc

databaseServer = 'dice-sql.database.windows.net'
databaseName = 'dice_sql_database'
databaseUsername = 'iAmRoot'
databasePassword = 'Qwerty@213'
connectionString = f'Driver={{ODBC Driver 17 for SQL Server}};Server=tcp:{databaseServer},1433;Database={databaseName};Uid={databaseUsername};Pwd={databasePassword};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'


conn = odbc.connect(connectionString)
cursor = conn.cursor()

# Fetch job queue
query = """
    SELECT TOP 20 id, title, description, company, dateUpdated 
    FROM allData 
    WHERE dateUpdated > 940704000
    ORDER BY dateUpdated DESC
"""
# cursor.execute(query)
# rows = cursor.fetchall()
# jobQueue = [{'id': row[0], 'title': row[1], 'description': row[2], 'company': row[3], 'timeOfArrival': str(row[4])} for row in rows]

# Fetch resume list
query = "SELECT * FROM resumeList"
cursor.execute(query)
rows = cursor.fetchall()
resumeData = {row[0]: row[1] for row in rows}

print(resumeData)
cursor.close()
conn.close()