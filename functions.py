import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def break_lines(texto, tamanho_maximo):
    palavras = texto.split()

    linhas = []

    linha_atual = ""

    for palavra in palavras:
        if len(linha_atual) + len(palavra) + 1 > tamanho_maximo:
            linhas.append(linha_atual)
            linha_atual = palavra
        else:
            if linha_atual:
                linha_atual += " " + palavra
            else:
                linha_atual = palavra

    if linha_atual:
        linhas.append(linha_atual)

    return "\n".join(linhas)


def veriry_keywords(keywords, title, text):
    for word in keywords:
        if word in title or word in text:
            return True
    return False


def send_email(subject, body, to_email):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    from_email = os.getenv("EMAIL_USER")
    from_password = os.getenv("EMAIL_PASSWORD")

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
    finally:
        server.quit()
