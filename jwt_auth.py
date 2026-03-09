import os
import mysql.connector
from jose import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

load_dotenv()

# Secret key
secret_KEY = os.getenv("SECRET_KEY")

# DB config
host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")

# DB connection
def get_connection():
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

# Bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# JWT
def create_token(data):
    expire = datetime.now(timezone.utc) + timedelta(hours=1)
    payload = {
        "user": data,
        "exp": expire
    }
    return jwt.encode(payload, secret_KEY, algorithm="HS256")

def verify_token(token):
    payload = jwt.decode(token, secret_KEY, algorithms=["HS256"])
    return payload

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/register", response_class=HTMLResponse)
def register(request: Request,
             name: str = Form(...),
             roll: int = Form(...),
             password: str = Form(...)):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM students WHERE roll=%s", (roll,))
    existing_student = cursor.fetchone()

    if existing_student:
        cursor.close()
        conn.close()
        return templates.TemplateResponse("login.html",
                                          {"request": request, "error": "Student already exists!"})

    hashed_pw = hash_password(password)
    cursor.execute("INSERT INTO students(name, roll, password) VALUES (%s, %s, %s)",
                   (name, roll, hashed_pw))
    conn.commit()
    cursor.close()
    conn.close()

    return templates.TemplateResponse("details_enter.html", {"request": request, "name": name})


@app.get("/exist", response_class=HTMLResponse)
def back_login(request: Request, name: str = ""):
    return templates.TemplateResponse("login.html", {"request": request, "name": name})


@app.get("/details_enter", response_class=HTMLResponse)
def show_details_enter(request: Request):
    return templates.TemplateResponse("details_enter.html", {"request": request})


@app.post("/submit", response_class=HTMLResponse)
def submit_form(request: Request,
                name: str = Form(...),
                roll: int = Form(...),
                password: str = Form(...)):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)      # ✅ একটাই dictionary cursor
    cursor.execute("SELECT * FROM students WHERE roll=%s", (roll,))
    student = cursor.fetchone()
    cursor.close()
    conn.close()

    if student and verify_password(password, student["password"]):
        token = create_token(roll)             # ✅ token বানাও
        response = templates.TemplateResponse(
            "show.html",
            {"request": request, "name": student["name"]}
        )
        response.set_cookie(key="access_token", value=token, httponly=True)  # ✅ cookie তে রাখো
        return response
    else:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid credential"}
        )


@app.get("/show", response_class=HTMLResponse)
def show(request: Request):
    token = request.cookies.get("access_token")   # ✅ 
    if not token:
        return RedirectResponse("/")              # ✅ 

    payload = verify_token(token)                
    roll = payload["user"]

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students WHERE roll=%s", (roll,))
    student = cursor.fetchone()
    cursor.close()
    conn.close()

    return templates.TemplateResponse("show.html", {"request": request, "name": student["name"]})