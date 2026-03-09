Student Login Page with FastAPI, JWT Authentication & Password Hashing

A simple student login system built with FastAPI, using JWT tokens for authentication and password hashing for secure storage. This project demonstrates modern authentication practices for Python web applications.

Features

✅ Student registration with hashed passwords using passlib.

✅ Login authentication with JWT tokens.

✅ Token verification for protected routes.

✅ Secure handling of sensitive data.

✅ MySQL integration for storing student data.

✅ HTML templates rendered with Jinja2 for frontend forms.

Technologies Used

FastAPI – Web framework for building APIs.

JWT (JSON Web Tokens) – Stateless authentication.

Passlib – Password hashing for security.

MySQL – Database for storing student information.

Jinja2 – Templating engine for HTML pages.

Python Dotenv – Load environment variables securely.

Installation

Clone the repository

git clone https://github.com/ayan-chakraborty242/student_login_form-with-JWT-auth-and-password-hashing.git
cd student_login_form-with-JWT-auth-and-password-hashing

Create and activate a virtual environment

python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

Install dependencies

pip install -r requirements.txt

Setup environment variables

Create a .env file:

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=student_login
SECRET_KEY=your_secret_key

Run the FastAPI server

uvicorn main:app --reload
Usage

Open your browser and go to:

http://127.0.0.1:8000/

Register a new student account with name, roll number, email, and password.

Login with roll number and password.

Access protected routes with your JWT token.

Project Structure
student_login/
│
├── main.py                # FastAPI app
├── JWt_auth.py            # JWT token creation & verification
├── templates/             # HTML templates (login, register, dashboard)
├── static/                # Static files (CSS/JS)
├── .env                   # Environment variables
└── requirements.txt       # Python dependencies
Security Features

Password Hashing – Passwords are never stored in plain text.

JWT Authentication – Tokens expire after a set duration for secure sessions.

Environment Variables – Sensitive data like DB credentials and secret keys are kept out of cod
