import os

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from datetime import datetime

import csv

from database.models import Base, Answer, Question, Users, Departments, Contacts

# Быстрое заполнение тестовой БД ---------------------------------------------------------------------------------------

DSN = os.environ.get("ONBOARDING_BOT_DB_DSN")
# DSN = 'postgresql://postgres:postgres@localhost:5432/onboarding_bot_db'
engine = sqlalchemy.create_engine(DSN)
# engine = create_engine("sqlite:///questions")
Session = sessionmaker(bind=engine)
session = Session()


date_format = "%Y-%m-%d"


def drop_tables():
    Base.metadata.drop_all(engine)
    print('Все таблицы удалены, все пропало !!!')


def create_tables():
    Base.metadata.create_all(engine)
    print('Таблицы созданы согласно models.py')


def null_or_date(string):
    if string != "NULL" and string != "":
        return datetime.strptime(string, date_format)
    else:
        return None


def null_or_not(string):
    if string != "NULL" and string != "":
        return string
    else:
        return None


def null_or_bool(string):
    if string != "NULL" and string != "":
        if string == "True":
            return True
        else:
            return False
    else:
        return None


def fill_db():
    drop_tables()
    create_tables()

    with open("temp/departments.csv", encoding="utf-8") as file:
        reader = csv.reader(x.replace('\0', '') for x in file)
        for row in reader:
            print(row)
            if row[0] != "id":
                new = Departments(
                    id=null_or_not(row[0]),
                    parent_id=null_or_not(row[1]),
                    name=null_or_not(row[2])
                )
                session.add(new)
                session.commit()

    with open("temp/users.csv", encoding="utf-8") as file:
        reader = csv.reader(x.replace('\0', '') for x in file)
        for row in reader:
            if row[0] != "id":
                print(row)
                new = Users(id=null_or_not(row[0]),
                            tg_id=null_or_not(row[1]),
                            tg_name=null_or_not(row[2]),
                            photo=null_or_not(row[3]),
                            hired_at=null_or_date(row[4]),
                            surname=null_or_not(row[5]),
                            first_name=null_or_not(row[6]),
                            middle_name=null_or_not(row[7]),
                            nickname=null_or_not(row[8]),
                            department_id=null_or_not(row[9]),
                            organization_id=null_or_not(row[10]),
                            user_id=null_or_not(row[11]),
                            fired_at=null_or_date(row[12]),
                            date_of_birth=null_or_date(row[13]),
                            job_title=null_or_not(row[14]),
                            status=null_or_not(row[15]),
                            timezone=null_or_not(row[16])
                            )
                session.add(new)
                session.commit()

    with open("temp/contacts.csv", encoding="utf-8") as file:
        reader = csv.reader(x.replace('\0', '') for x in file)
        for row in reader:
            print(row)
            if row[0] != "profile_id":
                new = Contacts(
                    profile_id=null_or_not(row[0]),
                    contact_type=null_or_not(row[1]),
                    contact=null_or_not(row[2]),
                    confirmed=null_or_bool(row[3])
                )
                session.add(new)
                session.commit()

    with open("temp/answers.csv", encoding="utf-8") as file:
        reader = csv.reader(x.replace('\0', '') for x in file)
        for row in reader:
            print(row)
            if row[0] != "id":
                new = Answer(
                    id=int(null_or_not(row[0])),
                    answer_text=null_or_not(row[1]),
                )
                session.add(new)
                session.commit()

    with open("temp/questions.csv", encoding="utf-8") as file:
        reader = csv.reader(x.replace('\0', '') for x in file)
        for row in reader:
            print(row)
            if row[0] != "id":
                new = Question(
                    id=int(null_or_not(row[0])),
                    question_text=null_or_not(row[1]),
                    id_answer=null_or_not(row[2]),
                )
                session.add(new)
                session.commit()

    session.close()


if __name__ == "__main__":
    fill_db()