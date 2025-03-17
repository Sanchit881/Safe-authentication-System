# Safe Authentication System (Flask)

This is a secure authentication system built using Flask, where users can register, log in, reset their password using an OTP (sent via email), and access a dashboard after logging in.

## Features
- **User Registration**: Users can sign up by providing their email, username, and password (password is hashed).
- **User Login**: Users can log in using their username and password.
- **Password Reset**: Users can reset their password via an OTP sent to their registered email.
- **Session Management**: Uses Flask sessions to manage user login state.
- **Dashboard**: After logging in, users are redirected to a dashboard with their profile information.

## Technologies Used
- **Flask**: Web framework for building the application.
- **MySQL**: Database for storing user data.
- **Werkzeug**: For password hashing and checking.
- **Flask-Mail**: For sending OTPs to users' email addresses.
- **HTML/CSS**: For frontend pages (login, registration, dashboard, etc.).

## Prerequisites

Make sure you have the following installed:

- **Python 3.x**
- **MySQL**: Ensure you have a MySQL database setup.
- **Flask**: Install Flask via pip (`pip install flask`).
- **Flask-Mail**: For sending emails (`pip install flask-mail`).
- **Werkzeug**: For password hashing (`pip install werkzeug`).
- **mysql-connector**: For MySQL database connection (`pip install mysql-connector`).

## Installation

Follow these steps to install and run the project locally:

### 1. Clone the repository

1. Clone the repository:
   ```bash
   git clone https://github.com/Sanchit881/safe-authentication-system.git
