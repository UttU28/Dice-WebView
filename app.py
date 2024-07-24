import pypyodbc as odbc
from flask import Flask, render_template, request, redirect, url_for
from credential import *
from datetime import datetime, timezone


app = Flask(__name__)

server = 'dice-sql.database.windows.net'
database = 'dice_sql_database'

connectionString = f'Driver={{ODBC Driver 17 for SQL Server}};Server=tcp:{server},1433;Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

global jobQueue
jobQueue = []
resumeData = {}

def fetch_initial_data():
    global jobQueue, resumeData
    try:
        conn = odbc.connect(connectionString)
        cursor = conn.cursor()

        # Fetch job queue
        query = """
            SELECT allData.id, allData.title, allData.description, allData.company, myQueue.timeOfArrival 
            FROM myQueue 
            JOIN allData ON myQueue.id = allData.id 
            ORDER BY myQueue.timeOfArrival ASC
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        jobQueue = [{'id': row[0], 'title': row[1], 'description': row[2], 'company': row[3], 'timeOfArrival': str(row[4])} for row in rows]

        # Fetch resume list
        query = "SELECT * FROM resumeList"
        cursor.execute(query)
        rows = cursor.fetchall()
        resumeData = {row[0]: row[1] for row in rows}

        cursor.close()
        conn.close()
    except odbc.Error as e:
        print(f"Error fetching initial data: {e}")


def removeFromQueue(jobID):
    try:
        conn = odbc.connect(connectionString)
        cursor = conn.cursor()
        query = "DELETE FROM myQueue WHERE id = ?"
        cursor.execute(query, [jobID])
        conn.commit()
        cursor.close()
        conn.close()
        print("Removed from the Queue")
    except odbc.Error as e:
        print(f"Error removing from queue: {e}")

def addToApplyQueue(jobID, selectedResume):
    try:
        conn = odbc.connect(connectionString)
        cursor = conn.cursor()
        timestamp = int(datetime.now(timezone.utc).timestamp())
        query = """INSERT INTO applyQueue (id, timeOfArrival, selectedResume)
                    SELECT ?, ?, ?
                    WHERE NOT EXISTS (
                        SELECT 1 FROM applyQueue WHERE id = ?
                    )"""
        params = (jobID, timestamp, selectedResume, jobID)
        cursor.execute(query, params)
        conn.commit()
        if cursor.rowcount != 1:
            print(f"JobID {jobID} already exists in apply queue. No duplicate added.")
        cursor.close()
        conn.close()
    except odbc.Error as e:
        print(f"Error adding to apply queue: {e}")

@app.route("/", methods=["GET", "POST"])
def home():
    global jobQueue

    if request.method == "POST":
        jobID = request.form.get("job_id")
        action = request.form.get("action")
        
        try:
            if action == "apply":
                resumeID = request.form.get("resume_id")
                addToApplyQueue(jobID, resumeID)
            removeFromQueue(jobID)

            jobQueue = [job for job in jobQueue if job['id'] != jobID]
        except Exception as e:
            print(f"Error processing form: {e}")

    if not jobQueue: fetch_initial_data()
    if not jobQueue: return render_template("jobNotFound.html")

    return render_template("index.html", jobData=jobQueue[0], resumeData=resumeData)

if __name__ == "__main__":
    fetch_initial_data()
    app.run(host="0.0.0.0", port=5500)
    # app.run()
