import os
from pprint import pprint

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from database.models import Base, Answer, Question, Users, Departments, Contacts, Projects, Operator_questions


class database:
    def __init__(self):

        DSN = os.environ.get("ONBOARDING_BOT_DB_DSN")
        # DSN = 'postgresql://postgres:postgres@localhost:5432/onboarding_bot_db'
        self.engine = sqlalchemy.create_engine(DSN)

        # self.engine = create_engine("sqlite:///questions")

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create_tables(self):
        Base.metadata.create_all(self.engine)
        print('Таблицы созданы согласно models.py')

    def drop_tables(self):
        Base.metadata.drop_all(self.engine)
        print('Все таблицы удалены, все пропало !!!')

    def close_session(self):
        self.session.close()

    def find_question_by_question_id(self, question_id: int) -> str:
        """
        Находит текст вопроса по его id в БД
        """
        question = self.session.query(Question).filter(Question.id == question_id).first()
        if question:
            return question.question_text
        else:
            return None

    def add_answer(self, answer: str):
        """
        Добавляет ответ в базу
        """
        new_answer = Answer(answer_text=answer)
        self.session.add(new_answer)
        self.session.commit()
        print(f'В БД добавлен ответ "{answer}" с id {new_answer.id}')
        return f'В БД добавлен ответ "{answer}" с id {new_answer.id}'

    def find_answer_by_text(self, text: str) -> int:
        """
        Принимает текст вопроса, возвращает его id
        """
        answers = self.session.query(Answer).filter(Answer.answer_text == text).first()
        return answers.id

    def find_answer_by_question_id(self, question_id):
        """
        Принимает id вопроса, возвращает текст ответа
        """
        result = self.session.query(Answer).join(Question).filter(Question.id == question_id).first()
        self.session.close()
        return result.answer_text

    def find_answer_by_answer_id(self, answer_id: int) -> object or None:
        """
        Находит ответ по его id, возвращает объект sqlalchemy
        """
        result = self.session.query(Answer).filter(Answer.id == answer_id).first()
        return result if result else None

    def find_all_answers(self):
        """
        Выводит словарь всех вопросов с их id
        """
        result = {}
        for answer in self.session.query(Answer).all():
            result[answer.id] = answer.answer_text
        return result

    def find_all_questions(self):
        """
        Отдает словарь со всеми вопросами для функции поиска
        """
        result = {}
        for i in self.session.query(Question).all():
            result[i.id] = i.question_text
        self.session.close()
        return result

    def add_question(self, question: str, answer_id: int):
        """
        Принимает текст вопроса и id ответа, добавляет вопрос в базу
        """
        answer = self.session.query(Answer).filter(Answer.id == answer_id).first()

        new_question = Question(question_text=question, id_answer=answer.id)
        self.session.add(new_question)
        self.session.commit()
        print(f'В БД добавлен вопрос "{question}" с id ответа {answer}')
        return f'В БД добавлен вопрос "{question}" с id ответа {answer}'

    def no_answer(self):
        """
        Возвращает вариант ответа под id 1
        """

        result = self.session.query(Answer).filter(Answer.id == 1).first()
        if result:
            return result.answer_text
        else:
            return None

    def find_by_surname(self, surname: str) -> list:
        """
        Поиск сотрудника по фамилии
        """
        result = []
        search = [i for i in self.session.query(Users).filter(Users.surname == surname).all()]
        for i in search:
            result.append({
                "id": i.id,
                "first_name": i.first_name,
                "surname": i.surname,
                "job_title": i.job_title
            })
        return result

    def partial_search_by_surname(self, surname: str) -> list:
        """
        Поиск сотрудника по частичному совпадению фамилии
        """
        result = []
        search = [i for i in self.session.query(Users).filter(Users.surname.ilike(f"%{surname}%")).all()]
        for i in search:
            result.append({
                "id": i.id,
                "first_name": i.first_name,
                "surname": i.surname,
                "job_title": i.job_title
            })
        return result

    def find_by_patronymic(self, patronimyc: str) -> list:
        """
        Поиск сотрудника по отчеству
        """
        result = []
        search = [i for i in self.session.query(Users).filter(Users.middle_name == patronimyc).all()]
        for i in search:
            result.append({
                "id": i.id,
                "first_name": i.first_name,
                "surname": i.surname,
                "job_title": i.job_title
            })
        return result

    def partial_search_by_patronymic(self, patronimyc: str) -> list:
        """
        Поиск сотрудника по частичному совпадению отчества
        """
        result = []
        search = [i for i in self.session.query(Users).filter(Users.middle_name.ilike(f"%{patronimyc}%")).all()]
        for i in search:
            result.append({
                "id": i.id,
                "first_name": i.first_name,
                "surname": i.surname,
                "job_title": i.job_title
            })
        return result

    def find_by_telegram_ninckname(self, telegram_ninckname: str) -> list:
        """
        Поиск сотрудника по telegram_ninckname
        """
        result = []
        search = [i for i in self.session.query(Users).filter(Users.tg_name == telegram_ninckname).all()]
        for i in search:
            result.append({
                "id": i.id,
                "first_name": i.first_name,
                "surname": i.surname,
                "job_title": i.job_title
            })
        return result

    def partial_search_by_telegram_ninckname(self, telegram_ninckname: str) -> list:
        """
        Поиск сотрудника по частичному совпадению telegram_ninckname
        """
        result = []
        search = [i for i in self.session.query(Users).filter(Users.tg_name.ilike(f"%{telegram_ninckname}%")).all()]
        for i in search:
            result.append({
                "id": i.id,
                "first_name": i.first_name,
                "surname": i.surname,
                "job_title": i.job_title
            })
        return result

    def find_by_email(self, email: str) -> list:
        result = []
        search = [i for i in self.session.query(Contacts).filter(Contacts.contact_type == "@"). \
            filter(Contacts.contact == email).all()]
        for i in search:
            user = self.__find_user_by_id(i.profile_id)
            result.append({
                "id": user.id,
                "first_name": user.first_name,
                "surname": user.surname,
                "job_title": user.job_title
            })
        return result

    def partial_search_by_email(self, email: str) -> list:
        result = []
        search = [i for i in self.session.query(Contacts).filter(Contacts.contact_type == "@"). \
            filter(Contacts.contact.ilike(f"%{email}%")).limit(10).all()]
        for i in search:
            user = self.__find_user_by_id(i.profile_id)
            result.append({
                "id": user.id,
                "first_name": user.first_name,
                "surname": user.surname,
                "job_title": user.job_title
            })
        return result

    def __find_user_by_id(self, id: int):
        result = self.session.query(Users).filter(Users.id == id).first()
        return result

    def find_department_by_user_id(self, user_id: int):
        """
        Находит отдел сотрудника по его id
        """
        result = self.session.query(Departments).join(Users.department).filter(Users.id == user_id).first()
        if result:
            return result.name

    def find_department_by_name(self, department: str) -> list:
        """
        Ищет отдел по названию
        """
        result = []
        search = [i for i in self.session.query(Departments).filter(Departments.name == department).all()]
        for i in search:
            employers = [i for i in self.session.query(Users).filter(Users.department_id == i.id).all()]
            result.append({
                "id": i.id,
                "name": i.name,
                "employers": [f"{i.first_name} {i.surname}" for i in employers]
            })
        return result

    def find_department_particial_by_name(self, department: str) -> list:
        """
        Ищет отдел по частичному совпадению названия
        """
        result = []
        search = [i for i in self.session.query(Departments).filter(Departments.name.ilike(f"%{department}%")).all()]
        for i in search:
            employers = [i for i in self.session.query(Users).filter(Users.department_id == i.id).all()]
            result.append({
                "id": i.id,
                "name": i.name,
                "employers": [f"{i.first_name} {i.surname}" for i in employers]
            })
        return result

    def find_by_title(self, title: str) -> list:
        """
        Находит сотрудника по должности
        """
        result = []
        search = self.session.query(Users).filter(Users.job_title == title).all()
        for i in search:
            result.append({
                "id": i.id,
                "first_name": i.first_name,
                "surname": i.surname,
                "job_title": i.job_title
            })
        return result

    def partial_search_by_title(self, title: str) -> list:
        """
        Находит сотрудника по частичному соответствию должности
        """
        result = []
        search = self.session.query(Users).filter(Users.job_title.ilike(f"%{title}%")).all()
        for i in search:
            result.append({
                "id": i.id,
                "first_name": i.first_name,
                "surname": i.surname,
                "job_title": i.job_title
            })
        return result

    def find_by_name(self, name: str) -> list:
        """
        Находит сотрудника по имени
        """
        result = []
        search = self.session.query(Users).filter(Users.first_name == name).all()
        for i in search:
            result.append({
                "id": i.id,
                "first_name": i.first_name,
                "surname": i.surname,
                "job_title": i.job_title
            })
        return result

    def partial_search_by_name(self, name: str) -> list:
        """
        Находит сотрудника по частичному соответствию имени
        """
        result = []
        search = self.session.query(Users).filter(Users.first_name.ilike(fr"%{name}%")).all()
        for i in search:
            result.append({
                "id": i.id,
                "first_name": i.first_name,
                "surname": i.surname,
                "job_title": i.job_title
            })
        return result

    def find_contacts_by_tg_id(self, tg_id: int) -> dict:
        """
        Находит ФИО и отдел пользователя по tg_id
        """
        result = {}
        search = self.session.query(Users).filter(Users.tg_id == tg_id).first()
        result["id"] = search.id
        result["first_name"] = search.first_name
        result["surname"] = search.surname
        result["job_title"] = search.job_title
        return result

    def find_contacts_by_id(self, id: int) -> dict:
        """
        Находит контакты пользователя по id
        """
        result = {}
        search = [i for i in self.session.query(Contacts).filter(Contacts.profile_id == id).all()]
        for i in search:
            if i.contact_type == "@":
                result["e-mail"] = i.contact
            elif i.contact_type == "P":
                result["phone"] = i.contact
        return result

    def find_all_users(self) -> list:
        """
        Отдает всех пользователей
        """
        result = []
        search = [i for i in self.session.query(Users).all()]
        for i in search:
            result.append({
                'telegram_id': i.tg_id,
                'Name': i.first_name,
                'Surname': i.surname,
                'Job_title': i.job_title,
            })

        return result

    def add_new_user(self, tg_id: int, first_name: str, surname: str, job_title: str, tg_name: str = None,
                     photo: str = None, hired_at: str = None, middle_name: str = None, nickname: str = None,
                     department_id: int = None, organization_id: int = None, user_id: int = None, fired_at: str = None,
                     date_of_birth: str = None, status: str = None, timezone: str = None):
        new_user = Users(
            tg_id=tg_id,
            first_name=first_name,
            surname=surname,
            job_title=job_title,
            tg_name=tg_name,
            photo=photo,
            hired_at=hired_at,
            middle_name=middle_name,
            nickname=nickname,
            department_id=department_id,
            organization_id=organization_id,
            user_id=user_id,
            fired_at=fired_at,
            date_of_birth=date_of_birth,
            status=status,
            timezone=timezone
        )
        self.session.add(new_user)
        self.session.commit()
        return f"Добавлен пользователь: {new_user.tg_id}"

    def is_tg_id_in_base(self, tg_id: int) -> bool:
        """
        Проверяет есть ли tg_id в базе бота
        """
        result = self.session.query(Users).filter(Users.tg_id == tg_id).first()
        if result:
            return True
        else:
            return False

    def particial_search_by_phone(self, phone: str) -> str or None:
        """
        Поиск по частичному совпадению номера телефона
        """
        result = self.session.query(Contacts).filter(Contacts.contact.ilike(f"%{phone}%")).first()
        if result:
            return self.__find_user_by_id(result.profile_id)
        else:
            return None

    def what_type_of_employment(self, tg_id: int) -> str or None:
        """
        Поиск способа трудоустройства
        """
        result = self.session.query(Users).filter(Users.tg_id == tg_id).first()
        return result.type_of_employment if result.type_of_employment else None

    def change_type_of_employment(self, tg_id: int, type_of_employement: str) -> bool:
        """
        Изменение типа трудоустройства
        """
        employer = self.session.query(Users).filter(Users.tg_id == tg_id).first()
        employer.type_of_employment = type_of_employement
        self.session.commit()
        self.session.close()
        return True

    def is_user(self, tg_id: int) -> bool:
        """
        Проверка существует ли пользователь в БД
        """
        result = self.session.query(Users).filter(Users.tg_id == tg_id).first()
        return True if result else False

    def all_projects(self) -> list:
        """
        Список всех проектов. Возвращает список объектов sqlalchemy
        """
        result = [i for i in self.session.query(Projects).all()]
        return result

    def find_project_text_by_id(self, project_id: int) -> str or None:
        """
        Ищет проект по id, возвращает текст для вывода в боте
        """
        result = self.session.query(Projects).filter(Projects.id == project_id).first()
        return result.bot_text if result.bot_text else None

    def add_new_operator_question(self, text: str, sender_tg_id: int) -> object:
        """
        Вносит новый вопрос для оператора в БД. Возвращает объект sqlalchemy с вопросом
        """
        new_question = Operator_questions(question_text=text, from_user_id=sender_tg_id)
        self.session.add(new_question)
        self.session.commit()
        return new_question

    def find_operator_question_by_id(self, id: int) -> str:
        """
        Возвращает текст вопроса оператору по его id
        """
        result = self.session.query(Operator_questions).filter(Operator_questions.id == id).first()
        return result.question_text