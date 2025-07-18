import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv('.env.local')

def send_email(to_email, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = os.getenv('EMAIL_FROM')
    msg['To'] = to_email
    
    with smtplib.SMTP(os.getenv('SMTP_SERVER'), int(os.getenv('SMTP_PORT'))) as server:
        server.starttls()
        server.login(os.getenv('EMAIL_FROM'), os.getenv('EMAIL_PASSWORD'))
        server.send_message(msg)

# Send to anyone
send_email(os.getenv('EMAIL_FROM'), 'Hello', 'Test message 2')
