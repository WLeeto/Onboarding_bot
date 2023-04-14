import smtplib
import os

from email.mime.text import MIMEText

from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


async def send_vacation_email(**kwargs):
    """
    Функция вызывается asincio.run() для отсутствия задержки при ответе gmail
    """
    sender = os.environ.get("SENDER_EMAIL")
    password = os.environ.get("SENDER_PASSWORD")
    if kwargs.get("superviser_email"):
        recipient = [os.environ.get("RECIPIENT_EMAIL")] + kwargs.get("superviser_email")
    else:
        recipient = os.environ.get("RECIPIENT_EMAIL")

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    text = f"Заявление на отпуск от: {kwargs.get('from_name')} {kwargs.get('from_surname')}\n" \
           f"Отдел: {kwargs.get('department_name')}\n\n" \
           f"Прошу принять заявление на отпуск в период: {kwargs.get('vacation_period')}\n" \
           f"Координатор: {kwargs.get('coordinator_name')}"
    subject = f"Отпуск {kwargs.get('from_name')} {kwargs.get('from_surname')} должность: {kwargs.get('job_title')}"

    msg = MIMEMultipart()
    msg['Subject'] = subject
    part = MIMEText(text)
    msg.attach(part)

    part = MIMEApplication(open(kwargs.get('image_path'), "rb").read())
    part.add_header("Content-Disposition", "attachment",
                    filename=f"{kwargs.get('from_name')} {kwargs.get('from_surname')}.jpg")
    msg.attach(part)

    try:
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())
        print("Message was sent")
        return True
    except Exception as _ex:
        print(_ex)
        return False


async def send_biz_trip_email(**kwargs):
    """
    """
    sender = os.environ.get("SENDER_EMAIL")
    password = os.environ.get("SENDER_PASSWORD")
    recipient = os.environ.get("BIZ_TRIP_RECIPIENT_EMAIL")

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    text = "Добрый день!\n" \
           f"В командировку направляется сотрудник: {kwargs.get('surname')} {kwargs.get('name')}\n" \
           f"Цель поездки: {kwargs.get('purpose')} \n" \
           f"Дата поездки: {kwargs.get('dates')}"
    subject = f"Командировка {kwargs.get('surname')} {kwargs.get('name')} {kwargs.get('dates')}"

    msg = MIMEMultipart()
    msg['Subject'] = subject
    part = MIMEText(text)
    msg.attach(part)

    part = MIMEApplication(open(kwargs.get('note_path'), "rb").read())
    part.add_header("Content-Disposition",
                    "attachment",
                    filename=f"{kwargs.get('surname')}_{kwargs.get('name')}_note.jpg")
    msg.attach(part)

    part = MIMEApplication(open(kwargs.get('advance_path'), "rb").read())
    part.add_header("Content-Disposition",
                    "attachment",
                    filename=f"{kwargs.get('surname')}_{kwargs.get('name')}_advance.jpg")
    msg.attach(part)

    part = MIMEApplication(open(kwargs.get('tickets_path'), "rb").read())
    part.add_header("Content-Disposition",
                    "attachment",
                    filename=f"{kwargs.get('surname')}_{kwargs.get('name')}_tickets.jpg")
    msg.attach(part)

    part = MIMEApplication(open(kwargs.get('checks_path'), "rb").read())
    part.add_header("Content-Disposition",
                    "attachment",
                    filename=f"{kwargs.get('surname')}_{kwargs.get('name')}_checks.jpg")
    msg.attach(part)

    try:
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())
        print("Message was sent")
        return True
    except Exception as _ex:
        print(_ex)
        return False


async def send_meeting_email(**kwargs):
    sender = os.environ.get("SENDER_EMAIL")
    password = os.environ.get("SENDER_PASSWORD")
    recipient = kwargs.get("recipient")

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    text = f"Добрый день!\n" \
           f"{kwargs.get('from_name')} приглашает вас принять участие во встрече:\n" \
           f"{kwargs.get('title')}\n" \
           f"Дата встречи:\n" \
           f"{kwargs.get('date')}\n\n" \
           f"Также уведомление придет вам в телеграм за 5 минут до начала"
    subject = f"Приглашение на встречу: {kwargs.get('title')}"

    msg = MIMEMultipart()
    msg['Subject'] = subject
    part = MIMEText(text)
    msg.attach(part)

    try:
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())
        print("Message was sent")
        return True
    except Exception as _ex:
        print(_ex)
        return False
