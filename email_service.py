import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_verification_email(to_email: str, code: str):
    msg = EmailMessage()
    msg["Subject"] = "Dine&Dash - Verify Your Email"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email

    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; text-align: center; padding: 20px;">
            <h2 style="color: #333;">Welcome to <span style="color: #ff6600;">Dine&Dash</span>! 🍽️</h2>
            <p style="font-size: 16px; color: #555;">Use the code below to verify your account:</p>
            <div style="display: inline-block; background: #ff6600; color: white; padding: 10px 20px; font-size: 20px; font-weight: bold; border-radius: 5px;">
                {code}
            </div>
            <p style="font-size: 14px; color: #777;">This code is valid for a limited time.</p>
        </body>
    </html>
    """

    msg.set_content(f"Your verification code is: {code}")
    msg.add_alternative(html_content, subtype="html")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(f"Error while sending the email: {e}")
        return False
