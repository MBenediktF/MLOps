import smtplib
import ssl
from dotenv import load_dotenv
import os
from helpers.logs import Log, ERROR, INFO
from email.utils import formatdate

load_dotenv()

mysql_user = os.getenv('MYSQL_USER')
mysql_password = os.getenv('MYSQL_USER_PASSWORD')
mysql_database = os.getenv('MYSQL_DATABASE')

smtp_server = os.getenv('EMAIL_SMTP_SERVER')
smtp_port = os.getenv('EMAIL_SMTP_PORT')
sender = os.getenv('EMAIL_SMTP_USER')
smtp_password = os.getenv('EMAIL_SMTP_PASSWORD')
receiver = os.getenv('EMAIL_RECIPIENT')


def send_email(subject: str, content: str) -> bool:
    log = Log()

    context = ssl.create_default_context()
    server = None

    message = (
        f"From: {sender}\n"
        f"To: {receiver}\n"
        f"Date: {formatdate()}\n"
        f"Subject: {subject}\n\n"
        f"{content}"
    )

    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port, context=context)
        server.login(sender, smtp_password)
        server.sendmail(sender, receiver, message)
        log.log(f"Email successfully sent to {receiver}", INFO)
    except Exception as e:
        log.log(f"Failed to send email: {e}", ERROR)
        return False
    finally:
        if server:
            server.quit()

    return True
