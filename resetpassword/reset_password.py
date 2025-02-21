# from fastapi import FastAPI, HTTPException, BackgroundTasks
# from send_email import send_email
# import random

# app = FastAPI()

# # Fake user data for testing
# fake_users_db = {
#     "maureen.koepp56@ethereal.email": {"id": 1, "password": "gYB9au7ZghaFsweZUb"}
# }

# # Store reset codes temporarily
# reset_codes = {}

# # 1️⃣ Request Password Reset (Sends Fake Email)
# @app.post("/request-reset")
# async def request_password_reset(email: str, background_tasks: BackgroundTasks):
#     if email not in fake_users_db:
#         raise HTTPException(status_code=404, detail="User not found")

#     reset_code = str(random.randint(100000, 999999))
#     reset_codes[email] = reset_code

#     # Send fake email
#     await send_email(background_tasks, email, reset_code)
#     return {"message": "Reset code sent"}

# # 2️⃣ Verify Code & Reset Password
# @app.post("/reset-password")
# async def reset_password(email: str, code: str, new_password: str):
#     if email not in fake_users_db:
#         raise HTTPException(status_code=404, detail="User not found")

#     if reset_codes.get(email) != code:
#         raise HTTPException(status_code=400, detail="Invalid or expired reset code")

#     # Simulate password update
#     fake_users_db[email]["password"] = new_password
#     del reset_codes[email]

#     return {"message": "Password reset successful"}

import json
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel, EmailStr, constr
from send_email import send_otp, otp_storage
from datetime import datetime

app = FastAPI()

USERS_FILE = "users.json"

# 🔹 Function to Load Users from JSON
def load_users():
    try:
        with open(USERS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# 🔹 Function to Save Users to JSON
def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)

class RequestResetSchema(BaseModel):
    email: EmailStr

class VerifyOTPAndResetSchema(BaseModel):
    email: EmailStr
    otp: str
    new_password: str
    confirm_password: str

# 📧 Route: Request OTP for Password Reset
@app.post("/request-reset/")
async def request_reset(data: RequestResetSchema, background_tasks: BackgroundTasks):
    users = load_users()
    email = data.email

    if email not in users:
        raise HTTPException(status_code=404, detail="User not found")

    background_tasks.add_task(send_otp, email)
    return {"message": "OTP has been sent to your email"}

# 🔹 Route: Verify OTP and Reset Password
@app.post("/verify-otp/")
async def verify_otp_and_reset(data: VerifyOTPAndResetSchema):
    users = load_users()
    email, otp, new_password, confirm_password = data.email, data.otp, data.new_password, data.confirm_password

    if new_password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    if email not in otp_storage:
        raise HTTPException(status_code=400, detail="OTP not requested")

    stored_otp_data = otp_storage[email]

    if datetime.utcnow() > stored_otp_data["expires_at"]:
        del otp_storage[email]
        raise HTTPException(status_code=400, detail="OTP expired")

    if stored_otp_data["otp"] != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    # ✅ Update Password and Save to JSON
    users[email]["password"] = new_password
    save_users(users)
    del otp_storage[email]

    return {"message": "Password reset successful!"}

