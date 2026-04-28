import os
import random
import base64
import smtplib
import mysql.connector

from typing import Optional
from fastapi import FastAPI, Form, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from email.mime.text import MIMEText
from passlib.hash import bcrypt

# =========================
# CONFIG
# =========================
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASS", ""),
    "database": os.getenv("DB_NAME", "portal_db")
}

EMAIL_USER = os.getenv("EMAIL_USER", "")
EMAIL_PASS = os.getenv("EMAIL_PASS", "")

ROLE_PREFIX = {
    "student": "std",
    "employee": "emp",
    "manager": "mgr",
    "entrepreneur": "ent",
    "jobseeker": "job"
}

# =========================
# APP
# =========================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # change to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# =========================
# MODELS
# =========================
class SignupData(BaseModel):
    name: str
    email: EmailStr
    role: str


class SigninData(BaseModel):
    login_id: str
    password: str


# =========================
# FUNCTIONS
# =========================
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def send_email(to_email, subject, body):
    if not EMAIL_USER or not EMAIL_PASS:
        return

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)


def generate_login_id(role):
    prefix = ROLE_PREFIX.get(role.lower(), "usr")
    digits = str(random.randint(10000, 99999))
    return f"{prefix}{digits}"


def generate_unique_login_id(role, cur):
    while True:
        login_id = generate_login_id(role)
        cur.execute("SELECT id FROM users WHERE login_id=%s", (login_id,))
        user = cur.fetchone()
        if not user:
            return login_id


# =========================
# ROUTES
# =========================
@app.get("/")
def home():
    return {"message": "API Running"}


# =========================
# SIGNUP
# =========================
@app.post("/api/signup")
def signup(data: SignupData):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    try:
        cur.execute("SELECT id FROM users WHERE email=%s", (data.email,))
        existing = cur.fetchone()

        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")

        login_id = generate_unique_login_id(data.role, cur)

        plain_password = str(random.randint(10000, 99999))
        hashed_password = bcrypt.hash(plain_password)

        cur.execute("""
            INSERT INTO users (name, email, login_id, password, role)
            VALUES (%s,%s,%s,%s,%s)
        """, (
            data.name,
            data.email,
            login_id,
            hashed_password,
            data.role
        ))

        conn.commit()

        send_email(
            data.email,
            "Your Login Details",
            f"""
Hello {data.name}

Role: {data.role}
Login ID: {login_id}
Password: {plain_password}
            """
        )

        return {
            "message": "Signup successful",
            "login_id": login_id
        }

    finally:
        cur.close()
        conn.close()


# =========================
# SIGNIN
# =========================
@app.post("/api/signin")
def signin(data: SigninData):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    try:
        cur.execute("SELECT * FROM users WHERE login_id=%s", (data.login_id,))
        user = cur.fetchone()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid login id")

        if not bcrypt.verify(data.password, user["password"]):
            raise HTTPException(status_code=401, detail="Wrong password")

        return {
            "user_id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
            "login_id": user["login_id"]
        }

    finally:
        cur.close()
        conn.close()


# =========================
# STUDENT PROFILE
# =========================
@app.post("/api/students")
def add_or_update_student(
    user_id: int = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    mobile: str = Form(...),
    gender: str = Form(...),
    current_location: str = Form(...),
    permanent_address: str = Form(...),
    college_name: str = Form(...),
    school_name: str = Form(...),
    photo: Optional[UploadFile] = File(None),
    resume: Optional[UploadFile] = File(None)
):
    photo_data = photo.file.read() if photo else None
    resume_data = resume.file.read() if resume else None

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    try:
        cur.execute("SELECT id FROM students WHERE user_id=%s", (user_id,))
        existing = cur.fetchone()

        if existing:
            query = """
            UPDATE students SET
            first_name=%s,
            last_name=%s,
            email=%s,
            mobile=%s,
            gender=%s,
            current_location=%s,
            permanent_address=%s,
            college_name=%s,
            school_name=%s
            """

            values = [
                first_name,
                last_name,
                email,
                mobile,
                gender,
                current_location,
                permanent_address,
                college_name,
                school_name
            ]

            if photo_data:
                query += ", photo=%s"
                values.append(photo_data)

            if resume_data:
                query += ", resume=%s"
                values.append(resume_data)

            query += " WHERE user_id=%s"
            values.append(user_id)

            cur.execute(query, tuple(values))

        else:
            cur.execute("""
            INSERT INTO students (
                user_id, first_name, last_name, email,
                mobile, gender, current_location,
                permanent_address, college_name,
                school_name, photo, resume
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                user_id,
                first_name,
                last_name,
                email,
                mobile,
                gender,
                current_location,
                permanent_address,
                college_name,
                school_name,
                photo_data,
                resume_data
            ))

        conn.commit()
        return {"message": "Saved successfully"}

    finally:
        cur.close()
        conn.close()


# =========================
# PROFILE
# =========================
@app.get("/api/profile/{user_id}")
def profile(user_id: int):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    try:
        cur.execute("SELECT id,name,email,role,login_id FROM users WHERE id=%s", (user_id,))
        user = cur.fetchone()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        cur.execute("SELECT * FROM students WHERE user_id=%s", (user_id,))
        student = cur.fetchone()

        if student:
            if student.get("photo"):
                student["photo"] = base64.b64encode(student["photo"]).decode()

            if student.get("resume"):
                student["resume"] = base64.b64encode(student["resume"]).decode()

        return {
            "user": user,
            "student": student
        }

    finally:
        cur.close()
        conn.close()
