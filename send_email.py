import smtplib, ssl
import os
import dotenv

dotenv.load_dotenv()
PASSWORD = os.getenv('PASSWORD')
USERNAME = os.getenv("USERNAME")


def send_mail(content):
    host = 'smtp.gmail.com'
    port = 465
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(USERNAME, PASSWORD)
        server.sendmail(USERNAME, USERNAME, msg=content)


if __name__ == "__main__":
    send_mail("Hi")
