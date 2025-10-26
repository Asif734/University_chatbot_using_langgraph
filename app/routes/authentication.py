# main.py
import os
import base64
from fastapi import FastAPI, APIRouter, HTTPException
from passlib.context import CryptContext
from app.schemas.authentication import SignUpRequest, OTPVerifyRequest, LoginRequest
from app.utils.authentication import generate_otp, send_otp_email, create_access_token
from app.db.database import (
    find_student,
    save_otp,
    get_otp,
    delete_otp,
    save_user,
    get_user_password,
    user_exists,
)

import hashlib

router = APIRouter()

def hash_password(password: str) -> str:
    """Create a salted SHA-256 hash."""
    salt = os.urandom(16)  # random 16-byte salt
    pwd_hash = hashlib.sha256(salt + password.encode()).digest()
    # store both salt and hash, base64 encoded
    return base64.b64encode(salt + pwd_hash).decode()

def verify_password(password: str, stored_hash: str) -> bool:
    """Verify password against stored salted hash."""
    decoded = base64.b64decode(stored_hash.encode())
    salt = decoded[:16]
    true_hash = decoded[16:]
    check_hash = hashlib.sha256(salt + password.encode()).digest()
    return check_hash == true_hash

# ------------------------
# 1. Sign Up: Send OTP
# ------------------------
@router.post("/signup")
def signup(data: SignUpRequest):
    # Check if student exists in students.json
    student = find_student(data.reg_id, data.email)
    if not student:
        raise HTTPException(status_code=400, detail="Invalid registration ID or email")

    # Check if already registered
    if user_exists(data.reg_id):
        raise HTTPException(status_code=400, detail="User already registered")

    # Generate OTP
    otp = generate_otp()
    save_otp(data.reg_id, otp)
    send_otp_email(data.email, otp)

    return {"message": f"OTP sent to {data.email}"}


# ------------------------
# 2. Verify OTP + Set Password
# ------------------------
@router.post("/verify-otp")
def verify_otp(data: OTPVerifyRequest):
    otp = get_otp(data.reg_id)

    if otp is None:
        raise HTTPException(status_code=400, detail="OTP not requested or expired")

    if otp != data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if data.password != data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # Save user
    hashed_pw = hash_password(data.password)
    save_user(data.reg_id, hashed_pw)
    delete_otp(data.reg_id)

    return {"message": "Registration successful! You can now log in."}


# ------------------------
# 3. Log In
# ------------------------
@router.post("/login")
def login(data: LoginRequest):
    if not user_exists(data.reg_id):
        raise HTTPException(status_code=400, detail="User not found")

    stored_hash = get_user_password(data.reg_id)
    if not stored_hash:
        raise HTTPException(status_code=400, detail="Password not set")

    # Verify password
    if not verify_password(data.password, stored_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")


    token = create_access_token(data.reg_id)

    return {"message": f"Login successful for {data.reg_id}","access_token": token}


