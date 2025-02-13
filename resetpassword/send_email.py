import random
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel, EmailStr
from typing import Dict
from datetime import datetime, timedelta

# 📧 Email Configuration
conf = ConnectionConfig(
    MAIL_USERNAME="nsttrung2004@gmail.com",
    MAIL_PASSWORD="xfihrjtixleyklrf",
    MAIL_FROM="darien.schamberger6@ethereal.email",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

# 🔹 Store OTPs temporarily (In production, use a database)
otp_storage: Dict[str, Dict] = {}

class EmailSchema(BaseModel):
    email: EmailStr

async def send_otp(email: str):
    otp = str(random.randint(100000, 999999))  # Generate 6-digit OTP
    otp_storage[email] = {
        "otp": otp,
        "expires_at": datetime.utcnow() + timedelta(minutes=5)  # OTP expires in 5 minutes
    }

    message = MessageSchema(
        subject="Password Reset OTP",
        recipients=[email],
        body=f"Your OTP for password reset is: {otp}. It is valid for 5 minutes.",
        subtype="plain",
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    return {"message": "OTP sent successfully!"}
