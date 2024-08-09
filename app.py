# Main application file
# app.py

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from config import AzureSQLConfig
from flask_bcrypt import Bcrypt
from utils.db_utils import *
from utils.email_utils import sendOtpEmail
import os, re
import random

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(AzureSQLConfig)

# Initialize bcrypt for password hashing
bcrypt = Bcrypt(app)

def update_html_content(description):
    keyWords = ['Snowflake', 'MongoDB', 'Azure VM']
    lowercase_keywords = sorted([kw.lower() for kw in keyWords], key=len, reverse=True)
    pattern = re.compile(r'\b(' + '|'.join(map(re.escape, lowercase_keywords)) + r')\b', re.IGNORECASE)

    def replace_keywords(match):
        keyword = match.group(0)
        return f"<span class='keyWord'>{keyword}</span>"

    description = pattern.sub(replace_keywords, description)
    description = description.replace('\n \n', '\n').replace('\n', '<br>')
    return description


# Home route
@app.route('/')
def index():
    if 'user' in session:
        jobData = loadJobsTill(session['lastView'])
        # resumeData = getUsersResumes(session['email'])
        resumeData = {1: 'AWS Utsav Chaudhary Resume.pdf', 2: 'Azure Utsav Chaudhary Resume.pdf', 3: 'DevOps SDE - Utsav Chaudhary.pdf', 4: 'GCP Utsav Chaudhary Resume.pdf', 5: 'GitHub Utsav Chaudhary Resume.pdf', 6: 'ML-DevOps Utsav Chaudhary Resume.pdf', 7: 'Utsav Chaudhary Resume-.pdf', 8: 'Utsav Chaudhary Resume.pdf'}

        if not jobData:
            return render_template("jobNotFound.html")
        for i in range(len(jobData)): jobData[i]["description"] = update_html_content(jobData[i]["description"])

        return render_template("index.html", jobData=jobData, resumeData=resumeData, pendingJobs=len(jobData))
        #     return render_template('index.html', user=session['user'], jobData=jobData)
        return render_template("jobNotFound.html")
    return redirect(url_for('login'))

@app.route('/jobAccepted', methods=['POST'])
def jobAccepted():
    jobID = request.form.get('jobID')
    selectedResume = request.form.get('selectedResume')
    lastView = request.form.get('lastView')

    print(jobID, selectedResume, lastView)
    if jobID:
        addToApplyQueue(jobID, selectedResume, session['email'])
        updateLastView(session['email'], lastView)
        return jsonify(success=True)
    return jsonify(success=False), 400

@app.route('/jobRejected', methods=['POST'])
def jobRejected():
    lastView = request.form.get('lastView')
    if lastView:
        updateLastView(session['email'], lastView)
        session['lastView'] = lastView
        return jsonify(success=True)
    return jsonify(success=False), 400

@app.route('/noMoreJobs')
def noMoreJobs():
    return render_template('jobNotFound.html')

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hashedPassword = bcrypt.generate_password_hash(password).decode('utf-8')

        existingUser = getUserByEmail(email)
        if existingUser:
            error = 'Email already registered. Please log in.'
            return render_template('register.html', error=error, name=name, email=email)
        
        createUser(name, email, hashedPassword)
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


# Login route
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
        
        # If login fails, return to the login page with an error message
        error = 'Invalid email or password. Please try again.'
        return render_template('login.html', error=error, email=email)
    
    return render_template('login.html')


# Logout route
@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('lastView', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# Forgot password route
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


# Reset password route
@app.route('/reset-password', methods=['GET', 'POST'])
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
    
    return render_template('reset_password.html')

if __name__ == '__main__':
    app.run(debug=True)
