import pypyodbc as odbc
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timezone
import re
import logging
import sys

app = Flask(__name__)

# Logging configuration
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

databaseServer = 'dice-sql.database.windows.net'
databaseName = 'dice_sql_database'
databaseUsername = 'iAmRoot'
databasePassword = 'Qwerty@213'
connectionString = f'Driver={{ODBC Driver 17 for SQL Server}};Server=tcp:{databaseServer},1433;Database={databaseName};Uid={databaseUsername};Pwd={databasePassword};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

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

        cursor.close()
        conn.close()
    except odbc.Error as e:
        logging.error(f"Error fetching initial data: {e}")


def removeFromQueue(jobID):
    try:
        conn = odbc.connect(connectionString)
        cursor = conn.cursor()
        query = "DELETE FROM allData WHERE id = ?"
        cursor.execute(query, [jobID])
        conn.commit()
        cursor.close()
        conn.close()
        logging.info("---------------------------------------Removed from the Queue")
    except odbc.Error as e:
        logging.error(f"Error removing from queue: {e}")

def addToApplyQueue(jobID, selectedResume):
    try:
        conn = odbc.connect(connectionString)
        cursor = conn.cursor()
        timestamp = int(datetime.now(timezone.utc).timestamp())
        query = """
            INSERT INTO applyQueue (id, timeOfArrival, selectedResume)
            SELECT ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM applyQueue WHERE id = ?
            );
        """
        params = (jobID, timestamp, selectedResume, jobID)
        cursor.execute(query, params)
        if cursor.rowcount != 1: logging.info(f"JobID {jobID} already exists in apply queue. No duplicate added.")
        else: logging.info("---------------------------------------Added to Apply Queue & Removed")
        query = "DELETE FROM allData WHERE id = ?"
        cursor.execute(query, [jobID])
        conn.commit()
        cursor.close()
        conn.close()
    except odbc.Error as e:
        logging.error(f"Error adding to apply queue: {e}")

def updateHTMLContent(thisDescription):
    keyWords = ['Snowflake', 'MongoDB', 'Azure VM', 'Logging', 'APIs', 'Kubernetes', 'Data Lakes', 'Postman', 'Extract', 'GCP Firebase', 'Apache Hadoop', 'JFrog Artifactory', 'AWS', 'Pipelines', 'Security vulnerability management', 'AngularJS', 'Azure SQL Database', 'Burp Suite', 'Bootstrap', 'Kali Linux', 'Monitoring tools', 'Apache Airflow', 'Google Cloud Platform', 'Angular', 'PyTorch', 'Scripting languages', 'AWS S3', 'Load', 'DataBricks', 'Linux shell scripting', 'Continuous Integration/Continuous Delivery', 'Groovy scripts', 'New Relic', 'Node.js', 'Azure Blob Storage', 'Docker containers', 'OWASP ZAP', 'Lean principles', 'ETL', 'Hibernate', 'Continuous Delivery', 'Continuous Improvement', 'Orchestration', 'AWS RDS', 'Java', 'Azure DevOps', 'Oracle', 'Puppet', 'Nagios', 'Grafana', 'Encryption methods', 'C#', 'Cassandra', 'Express.js', 'Data lineage', 'Apache Spark', 'JSON', 'PHP', 'GitOps', 'CI/CD', 'GitHub Actions', 'Blue-Green deployment', 'Mobile Device development', 'Data privacy', 'SQL', 'Agile', 'Python', 'Azure certifications', 'Django', 'ELK Stack', 'NGINX', 'React.js', 'Slack', 'NoSQL', 'Material UI', 'Compliance measures', 'Kibana', 'Scrum', 'GCP Cloud SQL', 'Azure Functions', 'SQL Server', 'Data governance', 'MySQL', 'Elasticsearch', 'Veracode', 'Azure Cosmos DB', 'REST APIs', 'Maven', 'Software Quality Assurance', 'Ansible', 'Microservices architecture', 'JavaScript', 'Windows PowerShell', 'Microservices', 'Vue.js', 'Nessus', 'Apache HTTP Server', 'Flask', 'RESTful APIs', 'Cloud computing', 'React', 'AWS Lambda', 'Azure services', 'ASP.NET', 'AWS services', 'TypeScript', 'Bash scripting', 'TensorFlow', 'Penetration testing', 'HTML', 'Powershell', 'Delta Lake', 'AWS EKS', 'Infrastructure as Code', 'CSS', 'Spring Boot', 'Splunk', 'GCP', 'Fortify', 'Spring Framework', 'ITIL', 'AWS CloudFormation', 'Apache Tomcat', 'NUnit', 'Azure Kubernetes Service', 'Transform', 'Docker', 'XML', 'Data Warehousing', 'Kanban', 'Data cataloging', 'AWS ECS', 'GCP Cloud Functions', 'Shift Left Security', 'Apache Kafka', 'Serverless architecture', 'Amazon Web Services', 'SOAP', 'Vulnerability management', 'Datadog', 'Bash', 'Containerization', 'Configuration management', 'GCP Compute Engine', 'JUnit', 'Continuous Integration', 'Continuous Development', 'Continuous Deployment', 'Network security', 'SonarQube', 'Canary deployment', 'GraphQL', '.NET Framework', 'PostgreSQL', 'OAuth', 'RESTful web services', 'DevSecOps', 'DevOps', 'Penetration Testing', 'Terraform', 'Git', 'Unix shell scripting', 'JIRA', 'Ruby on Rails', 'BigQuery', 'TestNG', 'Data warehousing', 'Power BI', 'GitHub', 'NoSQL databases', 'Metasploit', 'Prometheus', '.NET Core', 'Agile development', 'AWS DynamoDB', 'Identity and access management', 'Secure data communication', 'Bitbucket', 'Data analytics', 'AWS EC2', 'Chef', 'Next.js', 'GCP Cloud Storage', 'Azure security', 'GCP Kubernetes Engine', 'Six Sigma', 'Entity Framework', 'Cucumber', 'Jenkins', 'Confluence', 'Logstash', 'Appium', 'SDLC', 'JWT', 'Observability', 'YAML', 'Serverless architectures', 'Selenium', 'Redis', 'GitLab', 'Metadata management', 'Business intelligence']

    lowercase_keywords = sorted([kw.lower() for kw in keyWords], key=len, reverse=True)
    pattern = re.compile(r'\b(' + '|'.join(map(re.escape, lowercase_keywords)) + r')\b', re.IGNORECASE)

    def replace_keywords(match):
        keyword = match.group(0)
        return f"<span class='keyWord'>{keyword}</span>"
    thisDescription = pattern.sub(replace_keywords, thisDescription)
    thisDescription = thisDescription.replace('\n \n', '\n').replace('\n','<br>')
    return thisDescription 

@app.route("/", methods=["GET", "POST"])
def home():
    global jobQueue

    if request.method == "POST":
        jobID = request.form.get("job_id")
        action = request.form.get("action")
        
        try:
            logging.info(f'--------------------------------------- {action}')
            if action == "apply":
                resumeID = request.form.get("resume_id")
                addToApplyQueue(jobID, resumeID)
            else: removeFromQueue(jobID)

            jobQueue = [job for job in jobQueue if job['id'] != jobID]
        except Exception as e:
            logging.error(f"Error processing form: {e}")

    if not jobQueue: fetch_initial_data()
    if not jobQueue: return render_template("jobNotFound.html")
    
    thisQueue = jobQueue[0]
    tempDesc = thisQueue["description"]
    tempDesc = updateHTMLContent(tempDesc)
    thisQueue["description"] = tempDesc
    return render_template("index.html", jobData=thisQueue, resumeData=resumeData, pendingJobs=len(jobQueue))

if __name__ == "__main__":
    fetch_initial_data()
    app.run(host="0.0.0.0", port=5500)
    # app.run()
