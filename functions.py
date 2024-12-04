import os
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def veriry_keywords(keywords, title, text):
    for word in keywords:
        if word in title or word in text:
            return True
    return False


def is_date_today(date_text):
    try:
        date_obj = datetime.datetime.strptime(date_text, "%d/%m/%Y").date()
        return datetime.datetime.now().date() == date_obj
    except ValueError:
        return False


def send_email(title, subject, body, to_emails):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    from_email = os.getenv("EMAIL_USER")
    from_password = os.getenv("EMAIL_PASSWORD")

    to_emails = to_emails.split(", ")

    for email in to_emails:
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(from_email, from_password)
            text = msg.as_string()
            server.sendmail(from_email, to_emails, text)
            print(f"Email enviado para {email}: {title}")
        except Exception as e:
            print(f"Erro ao enviar e-mail para {email}: {e}")
        finally:
            server.quit()
