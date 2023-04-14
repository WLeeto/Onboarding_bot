import os

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from database.models import Base, Answer, Question, Users, Departments, Contacts, Projects, Operator_questions, \
    Newbie, New_User, Statistics, SuperviserEmployer


class database:
    def __init__(self):

        DSN = os.environ.get("ONBOARDING_BOT_DB_DSN")

        # DSN = 'postgresql://postgres:postgres@localhost:5432/onboarding_bot_db'

        self.engine = sqlalchemy.create_engine(DSN)
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

    def add_new_question_and_answer(self, question_text: str, answer_text: str, added_by_tg_id: int) -> None:
        """
        Добавляет в БД новый вопрос и ответ на него (для функции добавления вопроса оператором)
        """
        try:
            id_answer = max([i.id for i in self.session.query(Answer).all()]) + 1
        except ValueError:
            id_answer = 1
        new_answer = Answer(id=id_answer,
                            answer_text=answer_text,
                            added_by_tg_id=added_by_tg_id)
        id_question = max([i.id for i in self.session.query(Question).all()]) + 1
        new_question = Question(id=id_question,
                                question_text=question_text,
                                added_by_tg_id=added_by_tg_id,
                                answer=new_answer)
        self.session.add(new_question, new_answer)
        self.session.commit()
        print(f"В БД были добавлены вопрос {new_answer.answer_text} и ответ {new_question.question_text}")
        self.session.close()

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
        try:
            id_answer = max([i.id for i in self.session.query(Question).all()]) + 1
        except ValueError:
            id_answer = 1
        new_question = Question(id=id_answer, question_text=question, id_answer=answer.id)
        self.session.add(new_question)
        self.session.commit()
        print(f'В БД добавлен вопрос "{question}" с id ответа {answer}')
        return True

    def no_answer(self):
        """
        Возвращает вариант ответа под id 1
        """

        result = self.session.query(Answer).filter(Answer.id == 1).first()
        if result:
            return result.answer_text
        else:
            return None

    def find_by_surname(self, surname: str) -> list or False:
        """
        Поиск сотрудника по фамилии
        """
        result = [i for i in self.session.query(Users).filter(Users.surname == surname).all()]
        return result if result else False

    def partial_search_by_surname(self, surname: str) -> list or False:
        """
        Поиск сотрудника по частичному совпадению фамилии
        """
        result = [i for i in self.session.query(Users).filter(Users.surname.ilike(f"%{surname}%")).all()]
        return result if result else False

    def find_by_patronymic(self, patronimyc: str) -> list or False:
        """
        Поиск сотрудника по отчеству
        """
        result = [i for i in self.session.query(Users).filter(Users.middle_name == patronimyc).all()]
        return result if result else False

    def find_by_tg_id(self, tg_id: int) -> object or False:
        """
        Поиск сотрудника по tg_id
        """
        result = self.session.query(Users).filter(Users.tg_id == tg_id).first()
        return result if result is not None else False

    def partial_search_by_patronymic(self, patronimyc: str) -> list or False:
        """
        Поиск сотрудника по частичному совпадению отчества
        """
        result = [i for i in self.session.query(Users).filter(Users.middle_name.ilike(f"%{patronimyc}%")).all()]
        return result if result is not None else False

    def find_by_telegram_ninckname(self, telegram_ninckname: str) -> list or False:
        """
        Поиск сотрудника по telegram_ninckname
        """
        result = [i for i in self.session.query(Users).filter(Users.tg_name == telegram_ninckname).all()]
        return result if result else False

    def find_user_by_telegram_nickname(self, telegram_nickname: str) -> object or None:
        result = self.session.query(Users).filter(Users.tg_name == telegram_nickname).first()
        return result if result else None

    def partial_search_by_telegram_ninckname(self, telegram_ninckname: str) -> list or False:
        """
        Поиск сотрудника по частичному совпадению telegram_ninckname
        """
        result = [i for i in self.session.query(Users).filter(Users.tg_name.ilike(f"%{telegram_ninckname}%")).all()]
        return result if result else False

    def find_by_email(self, email: str) -> list or False:
        result = []
        search = [i for i in self.session.query(Contacts).filter(Contacts.contact_type == "@"). \
            filter(Contacts.contact == email).all()]
        for i in search:
            user = self.find_user_by_id(i.profile_id)
            result.append(user)
        return result if result else False

    def find_email_by_user_id(self, id: int) -> str or False:
        """
        Находит email пользователя по его id
        """
        result = self.session.query(Contacts) \
            .filter(Contacts.profile_id == id) \
            .filter(Contacts.contact_type == "@").first()
        return result.contact if result else False

    def partial_search_by_email(self, email: str) -> list or False:
        result = []
        search = [i for i in self.session.query(Contacts).filter(Contacts.contact_type == "@"). \
            filter(Contacts.contact.ilike(f"%{email}%")).limit(10).all()]
        for i in search:
            user = self.find_user_by_id(i.profile_id)
            result.append(user)
        return result if result else False

    def find_user_by_id(self, id: int):
        result = self.session.query(Users).filter(Users.id == id).first()
        return result

    def find_department_by_user_id(self, user_id: int):
        # todo удалить метод, исправить код в команде /find
        """
        Находит отдел сотрудника по его id
        """
        result = self.session.query(Departments).join(Users.department).filter(Users.id == user_id).first()
        if result:
            return result.name

    def find_department_obj_by_user_id(self, user_id: int) -> object or False:
        """
        Находит отдел сотрудника по его id
        """
        result = self.session.query(Departments).join(Users.department).filter(Users.id == user_id).first()
        if result:
            return result if result else False

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

    def find_by_title(self, title: str) -> list or False:
        """
        Находит сотрудника по должности
        """
        result = [i for i in self.session.query(Users).filter(Users.job_title == title).all()]
        return result if result else False

    def partial_search_by_title(self, title: str) -> list or False:
        """
        Находит сотрудника по частичному соответствию должности
        """
        result = [i for i in self.session.query(Users).filter(Users.job_title.ilike(f"%{title}%")).all()]
        return result if result else False

    def find_by_name(self, name: str) -> dict:
        """
        Находит сотрудника по имени
        """
        result = [i for i in self.session.query(Users).filter(Users.first_name == name).all()]
        return result if result else False

    def partial_search_by_name(self, name: str) -> list or False:
        """
        Находит сотрудника по частичному соответствию имени
        """
        result = [i for i in self.session.query(Users).filter(Users.first_name.ilike(fr"%{name}%")).all()]
        return result if result else False

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
                     date_of_birth: str = None, status: str = None, timezone: str = None,
                     type_of_employment: str = None, tg_photo: str = None, hobby: str = None) -> bool:

        try:
            id = max([i.id for i in self.session.query(Users).all()]) + 1
        except ValueError:
            id = 1

        try:
            new_user = Users(
                id=id,
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
                timezone=timezone,
                type_of_employment=type_of_employment,
                tg_photo=tg_photo,
                hobby=hobby,
            )
            self.session.add(new_user)
            self.session.commit()
            self.session.close()
            return True
        except IntegrityError as ex:
            self.session.close()
            print(ex)
            return False

    def is_tg_id_in_base(self, tg_id: int) -> bool:
        """
        Проверяет есть ли tg_id в базе бота
        """
        result = self.session.query(Users).filter(Users.tg_id == tg_id).first()
        if result:
            return True
        else:
            return False

    def particial_search_by_phone(self, phone: str) -> list or False:
        """
        Поиск по частичному совпадению номера телефона
        """
        result = []
        search = [i.profile_id for i in self.session.query(Contacts).filter(Contacts.contact.ilike(f"%{phone}%")).all()]
        for i in search:
            result.append(self.find_user_by_id(i))
        return result if result else False

    def what_type_of_employment(self, tg_id: int) -> str or None:
        """
        Поиск способа трудоустройства
        """
        result = self.session.query(Users).filter(Users.tg_id == tg_id).first()
        try:
            return result.type_of_employment
        except AttributeError:
            return None

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
        Проверка существует ли пользователь в БД по id телеграм
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

    def add_new_operator_question(self, question_text: str, sender_tg_id: int, message_id: int) -> object:
        """
        Вносит новый вопрос для оператора в БД. Возвращает объект sqlalchemy с вопросом
        """
        new_question = Operator_questions(question_text=question_text, from_user_id=sender_tg_id, message_id=message_id)
        self.session.add(new_question)
        self.session.commit()
        return new_question

    def find_operator_question_by_id(self, id: int) -> str:
        """
        Возвращает текст вопроса оператору по его id
        """
        result = self.session.query(Operator_questions).filter(Operator_questions.id == id).first()
        return result.question_text

    def all_answers(self) -> list or None:
        """
        Список всех объектов sqlalchemy ответов для генерации клавиатуры быстрых ответов
        """
        result = [i for i in self.session.query(Answer).all()]
        return result if result else None

    def add_newbie(self, newbie_tg_id: int, added_by_tg_id: int) -> bool:
        """
        Добавляет tg_id в список новеньких
        """
        try:
            id = max([i.id for i in self.session.query(Newbie).all()]) + 1
        except ValueError:
            id = 1
        try:
            newbie = Newbie(id=id, newbie_tg_id=newbie_tg_id, added_by_tg_id=added_by_tg_id)
            self.session.add(newbie)
            self.session.commit()
            self.session.close()
            return True
        except IntegrityError as ex:
            print(ex)
            self.session.close()
            return False

    def is_tg_id_in_newbie_base(self, tg_id: int) -> bool:
        result = self.session.query(Newbie).filter(Newbie.newbie_tg_id == tg_id).first()
        return True if result else False

    def add_new_contact(self, profile_id: int, contact_type: str, contact: str):

        try:
            id = max([i.id for i in self.session.query(Contacts).all()]) + 1
        except ValueError:
            id = 1
        try:
            new_contact = Contacts(
                id=id,
                profile_id=profile_id,
                contact_type=contact_type,
                contact=contact
            )
            self.session.add(new_contact)
            self.session.commit()
            self.session.close()
            return new_contact
        except IntegrityError as ex:
            self.session.close()
            print(ex)
            return False

    def add_newbie_for_confirming(self, **kwargs):
        newbee = New_User(
            tg_id=kwargs.get("tg_id"),
            first_name=kwargs.get("first_name"),
            surname=kwargs.get("surname"),
            middle_name=kwargs.get("middle_name"),
            job_title=kwargs.get("job_title"),
            tg_name=kwargs.get("tg_name"),
            date_of_birth=kwargs.get("date_of_birth"),
            hired_at=kwargs.get("hired_at"),
            type_of_employment=kwargs.get("type_of_employment"),
            phone=kwargs.get("phone"),
            email=kwargs.get("email"),
            tg_photo=kwargs.get("tg_photo"),
            hobby=kwargs.get("hobby"),
        )
        self.session.add(newbee)
        self.session.commit()
        self.session.close()

    def find_one_confirming_user(self, tg_id: int) -> object or False:
        """
        Найти пользователя в New_User для передачи данных от пользователя оператору.
        """
        result = self.session.query(New_User).filter(New_User.tg_id == tg_id).first()
        return result if result else False

    def clear_newbee_confirming(self, id: int):
        """
        Удаляет временную запись о новом сотруднике.
        """
        to_delete = self.session.query(New_User).filter(New_User.id == id).first()
        self.session.delete(to_delete)
        self.session.commit()

    def find_statistics(self, tg_id):
        result = self.session.query(Statistics).filter(Statistics.tg_id == tg_id).first()
        return True if result else False

    def add_statistics(self, tg_id):
        new_user = Statistics(tg_id=tg_id)
        self.session.add(new_user)
        self.session.commit()
        self.session.close()

    def find_superviser(self, department_id):
        res = self.session.query(SuperviserEmployer).filter(SuperviserEmployer.department_id == department_id).first()
        return res.superviser_id
