# services/email_service.py
import random
from flask_mail import Message
from ..extensions import mail

def generate_2fa_code():
    return f"{random.randint(100000, 999999)}"

def send_2fa_email(user_email, code):
    msg = Message(subject="Seu código de verificação 2FA",
                  recipients=[user_email],
                  body=f"Seu código de verificação é: {code}")
    mail.send(msg)
