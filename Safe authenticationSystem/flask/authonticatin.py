from flask import Flask, render_template, request, flash, redirect, url_for, session
import mysql.connector
from db_connection import create_connection
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import *
import random

app = Flask(__name__)
app.secret_key = 'login'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'sanchitchavan881@gmail.com'  # replace with your email
app.config['MAIL_PASSWORD'] = 'mlwf oacm vdmi nitb'

mail = Mail(app)
otp=random.randint(0000,9999)

# Create database connection
conn = create_connection()
cursor = conn.cursor(dictionary=True)

@app.route('/')
def home():
    return render_template('loginpro.html')  # Render the login page

@app.route('/regester', methods=['GET', 'POST'])
def regester():
    if request.method == 'POST':
        email = request.form.get('email')
        uname = request.form.get('username')
        password = request.form.get('password')

        # Hash the password using werkzeug.security
        hashed_password=generate_password_hash(password)

        # Insert into register table
        cursor.execute('INSERT INTO sanchit (email, username, password) VALUES (%s, %s, %s)', (email, uname, hashed_password))
        conn.commit()
        flash("You have successfully registered!")
        return redirect(url_for('regester')) 

    return render_template('regester.html')  # If GET request, render registration page

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Fetch user from the database
    cursor.execute('SELECT username, password FROM sanchit WHERE username = %s', (username,))
    user = cursor.fetchone()

    if user and check_password_hash(user['password'],password) :#Here, it checks if a user was found in the database 
    #and if the password the user entered matches the password stored in the database
       
        session['user_id'] = username #If the login is successful, the username is stored in the session.
    #The session keeps track of the user's login status across different pages. This is how the application knows the user 
    # is logged in and who they are
       
        return redirect(url_for('dashboard'))  # Redirect to dashboard if login is successful
    
    else:
        flash("Incorrect username or password", "danger")  # Show error message
        return redirect(url_for('home'))  # Redirect to the login page again if failed

@app.route('/dashboard')
def dashboard():
    # Ensure user is logged in
    if 'user_id' not in session:
        return redirect(url_for('home'))  # Redirect to login page if not logged in

    # Fetch user info from the database based on session's user_id
    username = session['user_id']
    cursor.execute('SELECT * FROM sanchit WHERE username = %s', (username,))
    user_info = cursor.fetchone()

    if user_info:
        return render_template('dashboard.html', user_info=user_info)  # Pass user info to the dashboard
    else:
        flash("User data not found", "danger")
        return redirect(url_for('home'))  # Redirect to login if no user info found

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user from session
    return redirect(url_for('home'))  # Redirect to login page after logging out
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password ():
        user_email = None

        if request.method == 'POST':
            email = request.form.get('email')
            cursor.execute('SELECT username FROM sanchit WHERE email = %s', (email,))
            user_email = cursor.fetchone()
            if user_email:
                session['user_email'] = email
                msg= Message('opt',sender='sanchitchavan881@gmail.com',recipients=[email])
                msg.body=str(otp)
                mail.send(msg) 
                flash("Email found! A password reset otp has been sent to your email.", "success")
                return redirect(url_for('verification'))  # redirecting to verifiction page
            else:
            # If email does not exist, flash an error message
                 flash("Email not found. Please check your email and try again.", "danger")
       
        return render_template('forgot_password.html')  # Render the forgot password page


@app.route('/verification', methods=['GET', 'POST'])
def verification ():
        if request.method == 'POST':
        # Logic to verify the code entered by the user
            code= request.form.get('verification_code')
        # Validate the code here
            if otp==int(code):  # This is a placeholder; you should generate a code dynamically
                flash("Verification successful!", "success")
                return redirect(url_for('resetpassword'))  # Redirect to reset password page
            else:
                 flash("Invalid verification code. Please try again.", "danger")
    
        return render_template('verification.html') 


@app.route('/resetpassword', methods=['GET', 'POST'])
def resetpassword():
    if 'user_email' not in session:
        flash("Please go through the verification process first.", "danger")
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # Ensure both passwords match
        if new_password == confirm_password:
            hashed_password=generate_password_hash(new_password)
            email=session['user_email'] 
            cursor.execute('UPDATE sanchit SET password = %s WHERE email = %s', (hashed_password, email))
            conn.commit()
            flash("Your password has been successfully reset.", "success")
            return redirect(url_for('home'))  # Redirect to the login page

        else:
            flash("Passwords do not match. Please try again.", "danger")
            return redirect(url_for('resetpassword'))  # Redirect back to reset password page

    return render_template('resetpassword.html')
   

if __name__ == '__main__':
    app.run(debug=True)
