# database.py
import json
from pathlib import Path
from typing import List, Dict, Any

BASE_DIR = Path(__file__).resolve().parent

STUDENT_FILE = BASE_DIR / "students.json"
USERS_FILE = BASE_DIR / "users.json"
OTP_FILE = BASE_DIR / "otp.json"


# ----------------------------
# Utility functions for JSON I/O
# ----------------------------
def read_json(file_path: Path) -> Any:
    if not file_path.exists():
        if file_path.suffix == ".json":
            file_path.write_text("[]", encoding="utf-8")
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(file_path: Path, data: Any):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ----------------------------
# Load students
# ----------------------------
def load_students() -> List[Dict[str, Any]]:
    return read_json(STUDENT_FILE)


def find_student(reg_id: str, email: str) -> Dict[str, str] | None:
    students = load_students()
    return next((s for s in students if s["reg_id"] == reg_id and s["email"] == email), None)


# ----------------------------
# Manage users (registered)
# ----------------------------
def load_users() -> Dict[str, Any]:
    data = read_json(USERS_FILE)
    return {item["reg_id"]: item for item in data}


def save_user(reg_id: str, hashed_password: str):
    users = read_json(USERS_FILE)
    # Remove old entry if exists
    users = [u for u in users if u["reg_id"] != reg_id]
    users.append({"reg_id": reg_id, "password": hashed_password})
    write_json(USERS_FILE, users)


def user_exists(reg_id: str) -> bool:
    users = read_json(USERS_FILE)
    return any(u["reg_id"] == reg_id for u in users)


def get_user_password(reg_id: str) -> str | None:
    users = read_json(USERS_FILE)
    user = next((u for u in users if u["reg_id"] == reg_id), None)
    return user["password"] if user else None


# ----------------------------
# Manage OTP store (optional file-based)
# ----------------------------
def save_otp(reg_id: str, otp: str):
    otps = read_json(OTP_FILE)
    otps = [o for o in otps if o["reg_id"] != reg_id]
    otps.append({"reg_id": reg_id, "otp": otp})
    write_json(OTP_FILE, otps)


def get_otp(reg_id: str) -> str | None:
    otps = read_json(OTP_FILE)
    record = next((o for o in otps if o["reg_id"] == reg_id), None)
    return record["otp"] if record else None


def delete_otp(reg_id: str):
    otps = read_json(OTP_FILE)
    otps = [o for o in otps if o["reg_id"] != reg_id]
    write_json(OTP_FILE, otps)
