import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, mapped_column

Base = declarative_base()


class Answer(Base):
    __tablename__ = "Answer"

    id = sq.Column(sq.Integer, primary_key=True)
    answer_text = sq.Column(sq.Text, nullable=True, unique=True)
    answer_discription = sq.Column(sq.Text)

    def __str__(self):
        return f'{self.id}: {self.answer_text}'


class Question(Base):
    __tablename__ = "Question"

    id = sq.Column(sq.Integer, primary_key=True)
    question_text = sq.Column(sq.Text, nullable=False, unique=True)
    id_answer = sq.Column(sq.Integer, sq.ForeignKey("Answer.id"), nullable=False)

    answer = relationship(Answer, backref="Question")

    def __str__(self):
        return f'{self.id}: {self.question_text}'


class Departments(Base):
    __tablename__ = "Departments"

    id = sq.Column(sq.Integer, primary_key=True)
    parent_id = sq.Column(sq.Integer)
    name = sq.Column(sq.Text)


class Users(Base):
    __tablename__ = "Users"

    id = sq.Column(sq.Integer, primary_key=True)
    tg_id = sq.Column(sq.BIGINT, nullable=False)
    tg_name = sq.Column(sq.Text)
    photo = sq.Column(sq.Text)
    hired_at = sq.Column(sq.Date)
    surname = sq.Column(sq.Text)
    first_name = sq.Column(sq.Text)
    middle_name = sq.Column(sq.Text)
    nickname = sq.Column(sq.Text)
    department_id = sq.Column(sq.Integer, sq.ForeignKey("Departments.id"))
    organization_id = sq.Column(sq.Integer)
    user_id = sq.Column(sq.Integer)
    fired_at = sq.Column(sq.Date)
    date_of_birth = sq.Column(sq.Date)
    job_title = sq.Column(sq.Text)
    status = sq.Column(sq.Text)
    timezone = sq.Column(sq.Text)
    type_of_employment = sq.Column(sq.Text)

    department = relationship(Departments, backref="Departments")


class Contacts(Base):
    __tablename__ = "Contacts"

    id = sq.Column(sq.Integer, primary_key=True)
    profile_id = sq.Column(sq.Integer, sq.ForeignKey("Users.id"))
    contact_type = sq.Column(sq.Text)
    contact = sq.Column(sq.Text)
    confirmed = sq.Column(sq.Boolean)

    user = relationship(Users, backref="Users")


class SuperviserEmployer(Base):
    __tablename__ = "SuperviserEmployer"

    id = sq.Column(sq.Integer, primary_key=True)
    superviser_id = mapped_column(sq.Integer, sq.ForeignKey("Users.id"))
    employer_id = mapped_column(sq.Integer, sq.ForeignKey("Users.id"))

    superviser = relationship(Users, foreign_keys=[superviser_id])
    employer = relationship(Users, foreign_keys=[employer_id])


class Projects(Base):
    __tablename__ = "Projects"

    id = sq.Column(sq.Integer, primary_key=True)
    project_name = sq.Column(sq.Text, nullable=False)
    bot_text = sq.Column(sq.Text, nullable=False)
    discription = sq.Column(sq.Text)


class Operator_questions(Base):
    __tablename__ = "Operator_questions"

    id = sq.Column(sq.Integer, primary_key=True)
    question_text = sq.Column(sq.Text)
    from_user_id = sq.Column(sq.BIGINT, nullable=False)
    message_id = sq.Column(sq.Integer, nullable=False)