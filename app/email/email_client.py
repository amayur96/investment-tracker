import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv('../../.env.local')

def send_email(to_email, subject, body, html=False):
    if html:
        from email.mime.multipart import MIMEMultipart
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = os.getenv('EMAIL_FROM')
        msg['To'] = to_email
        
        # Create text version
        text_content = "Please view this email in HTML format."
        text_part = MIMEText(text_content, 'plain')
        html_part = MIMEText(body, 'html')
        
        msg.attach(text_part)
        msg.attach(html_part)
    else:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = os.getenv('EMAIL_FROM')
        msg['To'] = to_email
    
    with smtplib.SMTP(os.getenv('SMTP_SERVER'), int(os.getenv('SMTP_PORT'))) as server:
        server.starttls()
        server.login(os.getenv('EMAIL_FROM'), os.getenv('EMAIL_PASSWORD'))
        server.send_message(msg)

# Send to anyone
#send_email(os.getenv('EMAIL_FROM'), 'Hello', 'Test message 2')
