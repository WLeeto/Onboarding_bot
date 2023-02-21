from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base, Answer, Question, Users, Departments, Contacts


class database:
    def __init__(self):
        self.engine = create_engine(f'sqlite:///{"questions"}')
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create_tables(self):
        Base.metadata.create_all(self.engine)
        print('Таблицы созданы согласно models.py')

    def drop_tables(self):
        Base.metadata.drop_all(self.engine)
        print('Все таблицы удалены, все пропало !!!')

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
        result = self.session.query(Answer).join(Question).filter(Question.id == question_id).first()
        self.session.close()
        return result.answer_text

    def find_all_answers(self):
        """
        Выводит список всех вопросов с их id
        """
        result = {}
        for answer in self.session.query(Answer).all():
            result[answer.id] = answer.answer_text
        return result

    def find_all_questions(self):
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
        return result.answer_text

    def find_by_surname(self, surname):
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

    def find_department_by_user_id(self, user_id):
        """
        Находит отдел сотрудника по его id
        """
        result = self.session.query(Departments).join(Users.department).filter(Users.id == user_id).first()
        return result.name

    def find_by_title(self, title) -> list:
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

    def find_contacts_by_id(self, user_id) -> dict:
        result = {}
        search = [i for i in self.session.query(Contacts).filter(Contacts.profile_id == user_id).all()]
        for i in search:
            if i.contact_type == "@":
                result["e-mail"] = i.contact
            elif i.contact_type == "P":
                result["phone"] = i.contact
        return result