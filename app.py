# Main application file
# app.py

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_from_directory
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from config import AzureSQLConfig
from utils.db_utils import *
from utils.storage_utils import *
from utils.email_utils import sendOtpEmail
import re, os
import random

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(AzureSQLConfig)

# Initialize bcrypt for password hashing
bcrypt = Bcrypt(app)


# File upload settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def update_html_content(description):
    keyWords = ['Snowflake', 'MongoDB', 'Azure VM', 'Logging', 'APIs', 'Kubernetes', 'Data Lakes', 'Postman', 'Extract', 'GCP Firebase', 'Apache Hadoop', 'JFrog Artifactory', 'AWS', 'Pipelines', 'Security vulnerability management', 'AngularJS', 'Azure SQL Database', 'Burp Suite', 'Bootstrap', 'Kali Linux', 'Monitoring tools', 'Apache Airflow', 'Google Cloud Platform', 'Angular', 'PyTorch', 'Scripting languages', 'AWS S3', 'Load', 'DataBricks', 'Linux shell scripting', 'Continuous Integration/Continuous Delivery', 'Groovy scripts', 'New Relic', 'Node.js', 'Azure Blob Storage', 'Docker containers', 'OWASP ZAP', 'Lean principles', 'ETL', 'Hibernate', 'Continuous Delivery', 'Continuous Improvement', 'Orchestration', 'AWS RDS', 'Java', 'Azure DevOps', 'Oracle', 'Puppet', 'Nagios', 'Grafana', 'Encryption methods', 'C#', 'Cassandra', 'Express.js', 'Data lineage', 'Apache Spark', 'JSON', 'PHP', 'GitOps', 'CI/CD', 'GitHub Actions', 'Blue-Green deployment', 'Mobile Device development', 'Data privacy', 'SQL', 'Agile', 'Python', 'Azure certifications', 'Django', 'ELK Stack', 'NGINX', 'React.js', 'Slack', 'NoSQL', 'Material UI', 'Compliance measures', 'Kibana', 'Scrum', 'GCP Cloud SQL', 'Azure Functions', 'SQL Server', 'Data governance', 'MySQL', 'Elasticsearch', 'Veracode', 'Azure Cosmos DB', 'REST APIs', 'Maven', 'Software Quality Assurance', 'Ansible', 'Microservices architecture', 'JavaScript', 'Windows PowerShell', 'Microservices', 'Vue.js', 'Nessus', 'Apache HTTP Server', 'Flask', 'RESTful APIs', 'Cloud computing', 'React', 'AWS Lambda', 'Azure services', 'ASP.NET', 'AWS services', 'TypeScript', 'Bash scripting', 'TensorFlow', 'Penetration testing', 'HTML', 'Powershell', 'Delta Lake', 'AWS EKS', 'Infrastructure as Code', 'CSS', 'Spring Boot', 'Splunk', 'GCP', 'Fortify', 'Spring Framework', 'ITIL', 'AWS CloudFormation', 'Apache Tomcat', 'NUnit', 'Azure Kubernetes Service', 'Transform', 'Docker', 'XML', 'Data Warehousing', 'Kanban', 'Data cataloging', 'AWS ECS', 'GCP Cloud Functions', 'Shift Left Security', 'Apache Kafka', 'Serverless architecture', 'Amazon Web Services', 'SOAP', 'Vulnerability management', 'Datadog', 'Bash', 'Containerization', 'Configuration management', 'GCP Compute Engine', 'JUnit', 'Continuous Integration', 'Continuous Development', 'Continuous Deployment', 'Network security', 'SonarQube', 'Canary deployment', 'GraphQL', '.NET Framework', 'PostgreSQL', 'OAuth', 'RESTful web services', 'DevSecOps', 'DevOps', 'Penetration Testing', 'Terraform', 'Git', 'Unix shell scripting', 'JIRA', 'Ruby on Rails', 'BigQuery', 'TestNG', 'Data warehousing', 'Power BI', 'GitHub', 'NoSQL databases', 'Metasploit', 'Prometheus', '.NET Core', 'Agile development', 'AWS DynamoDB', 'Identity and access management', 'Secure data communication', 'Bitbucket', 'Data analytics', 'AWS EC2', 'Chef', 'Next.js', 'GCP Cloud Storage', 'Azure security', 'GCP Kubernetes Engine', 'Six Sigma', 'Entity Framework', 'Cucumber', 'Jenkins', 'Confluence', 'Logstash', 'Appium', 'SDLC', 'JWT', 'Observability', 'YAML', 'Serverless architectures', 'Selenium', 'Redis', 'GitLab', 'Metadata management', 'Business intelligence']
    lowercase_keywords = sorted([kw.lower() for kw in keyWords], key=len, reverse=True)
    pattern = re.compile(r'\b(' + '|'.join(map(re.escape, lowercase_keywords)) + r')\b', re.IGNORECASE)

    def replace_keywords(match):
        keyword = match.group(0)
        return f"<span class='keyWord'>{keyword}</span>"

    description = pattern.sub(replace_keywords, description)
    description = description.replace('\n \n', '\n').replace('\n', '<br>')
    return description

# Routes

# Home route
@app.route('/')
def index():
    if 'user' in session:
        session['lastView'] = getUserLastView(session['email'])
        jobData = loadJobsTill(session['lastView'])
        # Dummy resume data for demonstration
        resumeData = {
            1: 'AWS Utsav Chaudhary Resume.pdf', 2: 'Azure Utsav Chaudhary Resume.pdf',
            3: 'DevOps SDE - Utsav Chaudhary.pdf', 4: 'GCP Utsav Chaudhary Resume.pdf',
            5: 'GitHub Utsav Chaudhary Resume.pdf', 6: 'ML-DevOps Utsav Chaudhary Resume.pdf',
            7: 'Utsav Chaudhary Resume-.pdf', 8: 'Utsav Chaudhary Resume.pdf'
        }
        resumeData = getUsersResumes(session['email'])

        if not jobData:
            return render_template("jobNotFound.html")
        for job in jobData:
            job["description"] = update_html_content(job["description"])

        return render_template("index.html", jobData=jobData, resumeData=resumeData, pendingJobs=len(jobData), user=session['user'], userEmail=session['email'])
    
    return redirect(url_for('login'))

# Job Actions
@app.route('/jobAccepted', methods=['POST'])
def jobAccepted():
    jobID = request.form.get('jobID')
    selectedResume = request.form.get('selectedResume')
    lastView = request.form.get('lastView')

    if jobID:
        session['lastView'] = lastView
        addToApplyQueue(jobID, selectedResume, session['email'])
        updateLastView(session['email'], lastView)
        return jsonify(success=True)
    
    return jsonify(success=False), 400

@app.route('/jobRejected', methods=['POST'])
def jobRejected():
    lastView = request.form.get('lastView')

    if lastView:
        session['lastView'] = lastView
        updateLastView(session['email'], lastView)
        return jsonify(success=True)
    
    return jsonify(success=False), 400

@app.route('/noMoreJobs')
def noMoreJobs():
    return render_template('jobNotFound.html')

# User Authentication
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hashedPassword = bcrypt.generate_password_hash(password).decode('utf-8')

        if getUserByEmail(email):
            error = 'Email already registered. Please log in.'
            return render_template('register.html', error=error, name=name, email=email)
        
        createUser(name, email, hashedPassword)
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = getUserByEmail(email)
        if user and bcrypt.check_password_hash(user['hashed_password'], password):
            session['user'] = user['name']
            session['email'] = user['email']
            session['lastView'] = user['last_view']
            return redirect(url_for('index'))
        
        error = 'Invalid email or password. Please try again.'
        return render_template('login.html', error=error, email=email)
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('lastView', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# Password Recovery
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgotPassword():
    if request.method == 'POST':
        email = request.form['email']
        user = getUserByEmail(email)
        if user:
            otp = str(random.randint(1000, 9999))
            session['otp'] = otp
            session['email'] = email
            sendOtpEmail(email, otp)
            flash('An OTP has been sent to your email. Please check your inbox.', 'info')
            return redirect(url_for('resetPassword'))
        
        error = 'Email not found. Please try again.'
        return render_template('forgot_password.html', error=error, email=email)

    return render_template('forgot_password.html')

@app.route('/resetPassword', methods=['GET', 'POST'])
def resetPassword():
    if request.method == 'POST':
        otp = request.form['otp']
        newPassword = request.form['new_password']
        
        if otp == session.get('otp'):
            hashedPassword = bcrypt.generate_password_hash(newPassword).decode('utf-8')
            updatePassword(session['email'], hashedPassword)
            flash('Your password has been reset successfully.', 'success')
            session.pop('otp', None)
            session.pop('email', None)
            return redirect(url_for('login'))
        
        flash('Invalid OTP. Please try again.', 'danger')
    
    return render_template('resetPassword.html')


@app.route('/resumes', methods=['GET', 'POST'])
def manageResume():
    if 'user' not in session:
        return redirect(url_for('login'))

    email = session['email']
    
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            resumeName = file.filename
            resumeID = upload_to_blob(file, str(datetime.now(timezone.utc).timestamp()).replace('.','') + str(random.randint(100,999)))
            # file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # file.save(file_path)

            
            # Add to database
            addResumeToDatabase(resumeID, resumeName, email)
            flash('Resume uploaded successfully!', 'success')
            return redirect(url_for('manageResume'))

    resumes = getUsersResumes(email)
    return render_template('manageResume.html', resumes=resumes)

@app.route('/delete_resume/<int:resume_id>')
def delete_resume(resume_id):
    deleteResumeFromDatabase(resume_id)
    flash('Resume deleted successfully!', 'success')
    return redirect(url_for('manageResume'))


if __name__ == '__main__':
    # app.run(debug=True, host="0.0.0.0", port=5000)
    app.run()
