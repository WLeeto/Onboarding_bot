from datetime import datetime

import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, mapped_column

Base = declarative_base()


class Answer(Base):
    __tablename__ = "Answer"

    id = sq.Column(sq.Integer, primary_key=True)
    answer_text = sq.Column(sq.Text, nullable=True, unique=True)
    answer_discription = sq.Column(sq.Text)
    added_by_tg_id = sq.Column(sq.BIGINT)

    def __str__(self):
        return f'{self.id}: {self.answer_text}'


class Question(Base):
    __tablename__ = "Question"

    id = sq.Column(sq.Integer, primary_key=True)
    question_text = sq.Column(sq.Text, nullable=False, unique=True)
    id_answer = sq.Column(sq.Integer, sq.ForeignKey("Answer.id"), nullable=False)
    added_by_tg_id = sq.Column(sq.BIGINT)

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
    tg_photo = sq.Column(sq.Text)
    hobby = sq.Column(sq.Text)

    department = relationship(Departments, backref="Departments")


class Organization(Base):
    __tablename__ = "Organization"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.Text, nullable=False)


class UserOrganization(Base):
    __tablename__ = "UserOrganization"

    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey("Users.id"))
    organization_id = sq.Column(sq.Integer, sq.ForeignKey("Organization.id"))

    user = relationship(Users, backref="UserOrganization")
    organization = relationship(Organization, backref="UserOrganization")


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
    superviser_id = sq.Column(sq.Integer, sq.ForeignKey("Users.id"))
    department_id = sq.Column(sq.Integer, sq.ForeignKey("Departments.id"))

    superviser = relationship(Users, backref="superviser")
    department = relationship(Departments, backref="superviser_department")


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


class Newbie(Base):
    __tablename__ = "Newbie"

    id = sq.Column(sq.Integer, primary_key=True)
    newbie_tg_id = sq.Column(sq.BIGINT, nullable=False, unique=True)
    added_by_tg_id = sq.Column(sq.BIGINT)
    created_at = sq.Column(sq.DateTime, default=datetime.now)
    updated_at = sq.Column(sq.DateTime, default=datetime.now, onupdate=datetime.now)


class New_User(Base):
    __tablename__ = "New_User"

    id = sq.Column(sq.Integer, primary_key=True)
    tg_id = sq.Column(sq.BIGINT)
    first_name = sq.Column(sq.Text)
    surname = sq.Column(sq.Text)
    middle_name = sq.Column(sq.Text)
    job_title = sq.Column(sq.Text)
    tg_name = sq.Column(sq.Text)
    date_of_birth = sq.Column(sq.Date)
    hired_at = sq.Column(sq.Date)
    type_of_employment = sq.Column(sq.Text)
    phone = sq.Column(sq.Text)
    email = sq.Column(sq.Text)
    tg_photo = sq.Column(sq.Text)
    hobby = sq.Column(sq.Text)


class Statistics(Base):
    __tablename__ = "Statistics"

    id = sq.Column(sq.Integer, primary_key=True)
    tg_id = sq.Column(sq.BIGINT)
    created_at = sq.Column(sq.DateTime, default=datetime.now)


class Full_statistics(Base):
    __tablename__ = "Full_statistics"

    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey("Users.id"))
    tg_id = sq.Column(sq.BIGINT, nullable=False)
    created_at = sq.Column(sq.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    command_used = sq.Column(sq.Text)
    text_request = sq.Column(sq.Text)
    is_answered = sq.Column(sq.Boolean)

    user = relationship(Users, backref="user_statistics")


class Schelduled_message(Base):
    __tablename__ = "Schelduled_message"

    id = sq.Column(sq.Integer, primary_key=True)
    text = sq.Column(sq.Text, nullable=False)
    from_id = sq.Column(sq.Integer, sq.ForeignKey("Users.id"))
    to_id = sq.Column(sq.Integer, sq.ForeignKey("Users.id"))
    date_to_send = sq.Column(sq.DateTime, nullable=False)

    from_user = relationship(Users, backref="from_user", foreign_keys=[from_id])
    to_user = relationship(Users, backref="to_user", foreign_keys=[to_id])