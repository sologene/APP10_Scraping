import smtplib, ssl
import os


def send_email(message):
    host = "smtp.gmail.com"
    port = 465
    password = os.getenv("PASSWORD")
    username = "website.contact34@gmail.com"
    receiver = "website.contact34@gmail.com"
    print(message)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)



