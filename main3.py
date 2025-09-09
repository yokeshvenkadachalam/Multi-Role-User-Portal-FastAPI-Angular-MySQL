from fastapi import FastAPI, Form, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import mysql.connector, random, smtplib, base64
from email.mime.text import MIMEText
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Yokesh@123",
    "database": "portal_db"
}
EMAIL_USER = "yokeshvenkadachalam@gmail.com"
EMAIL_PASS = "dkvs aktz dfxs tfzm"
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)
ROLE_PREFIX = {
    "student": "std",
    "employee": "emp",
    "manager": "mgr",
    "entrepreneur": "ent",
    "jobseeker": "job"
}
class SignupData(BaseModel):
    name: str
    email: str
    role: str

class SigninData(BaseModel):
    login_id: str
    password: str

def send_email(to, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = to
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)

def generate_login_id(role: str) -> str:
    prefix = ROLE_PREFIX.get(role.lower(), "usr")
    digits = str(random.randint(10000, 99999))
    return f"{prefix}{digits}"

@app.post("/api/signup")
def signup(data: SignupData):
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute("SELECT id FROM users WHERE email=%s", (data.email,))
        existing = cur.fetchone()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")

        login_id = generate_login_id(data.role)
        password = str(random.randint(10000, 99999))  
        cur.execute(
            "INSERT INTO users (name, email, login_id, password, role) VALUES (%s,%s,%s,%s,%s)",
            (data.name, data.email, login_id, password, data.role)
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()
    send_email(
        data.email,
        "Your Portal Login Credentials",
        f"Hello {data.name},\n\n"
        f"Your account has been created with the following details:\n\n"
        f"Role: {data.role}\n"
        f"Login ID: {login_id}\n"
        f"Password: {password}\n\n"
        f"Use these credentials to sign in to the portal."
    )

    return {"message": f"Signup successful. Credentials sent to {data.email}", "login_id": login_id}

@app.post("/api/signin")
def signin(data: SigninData):
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute("SELECT * FROM users WHERE login_id=%s AND password=%s", (data.login_id, data.password))
        user = cur.fetchone()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    finally:
        cur.close()
        conn.close()
    return {
        "user_id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
        "login_id": user["login_id"],
    }

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

    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute("SELECT id FROM students WHERE user_id=%s", (user_id,))
        existing = cur.fetchone()
        if existing:
            cur.execute("""
                UPDATE students
                SET first_name=%s, last_name=%s, email=%s, mobile=%s, gender=%s,
                    current_location=%s, permanent_address=%s, college_name=%s, school_name=%s,
                    photo=%s, resume=%s
                WHERE user_id=%s
            """, (
                first_name, last_name, email, mobile, gender, current_location, permanent_address,
                college_name, school_name, photo_data, resume_data, user_id
            ))
        else:
            cur.execute("""
                INSERT INTO students
                (user_id, first_name, last_name, email, mobile, gender, current_location,
                 permanent_address, college_name, school_name, photo, resume)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                user_id, first_name, last_name, email, mobile, gender, current_location,
                permanent_address, college_name, school_name, photo_data, resume_data
            ))
        conn.commit()
    finally:
        cur.close()
        conn.close()
    return {"message": "Student details saved/updated."}

@app.get("/api/profile/{user_id}")
def profile(user_id: int):
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute("SELECT id, name, email, role FROM users WHERE id=%s", (user_id,))
        user = cur.fetchone()
        cur.execute("SELECT * FROM students WHERE user_id=%s", (user_id,))
        student = cur.fetchone()
        if student:
            if student.get("photo"):
                student["photo"] = base64.b64encode(student["photo"]).decode()
            if student.get("resume"):
                student["resume"] = base64.b64encode(student["resume"]).decode()
    finally:
        cur.close()
        conn.close()
    return {"user": user, "student": student}
