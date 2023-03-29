import smtplib
import os
import asyncio

from email.mime.text import MIMEText
from email.header import Header

from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


async def send_vacation_email(from_name, from_surname, job_title, vacation_period, is_agreed,
                              coordinator_name, image_path):
    """
    Функция вызывается asincio.run() для отсутствия задержки при ответе gmail
    """
    sender = os.environ.get("SENDER_EMAIL")
    password = os.environ.get("SENDER_PASSWORD")
    recipient = os.environ.get("RECIPIENT_EMAIL")

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    text = f"Прошу принять заявление на отпуск в период {vacation_period}\n" \
           f"Отпуск с уководителем согласован: {is_agreed}\n" \
           f"Координатор: {coordinator_name}"
    subject = f"Отпуск {from_name} {from_surname} должность: {job_title}"

    msg = MIMEMultipart()
    msg['Subject'] = subject
    part = MIMEText(text)
    msg.attach(part)

    part = MIMEApplication(open(image_path, "rb").read())
    part.add_header("Content-Disposition", "attachment", filename=f"{from_name} {from_surname}.jpg")
    msg.attach(part)

    try:
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())
        print("Message was sent")
        return True
    except Exception as _ex:
        return f"{_ex}\nMessage wasn't sent !!!"


async def send_biz_trip_email(**kwargs):
    """
    """
    sender = os.environ.get("SENDER_EMAIL")
    password = os.environ.get("SENDER_PASSWORD")
    recipient = os.environ.get("RECIPIENT_EMAIL")  # todo поменять получателя, запросить у Розы

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