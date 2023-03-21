from aiogram.dispatcher.filters.state import StatesGroup, State


class FSM_newbie_questioning(StatesGroup):
    newbie_questioning_start = State()
    asking_surname = State()
    email_creating = State()
    asking_surname_eng = State()
    asking_bday = State()
    asking_phone = State()
    asking_email = State()
    asking_photo = State()
    asking_hobby = State()
    commit_data = State()
    show_video = State()
    accept_new_user = State()
    save_job_title = State()
    save_type_of_employement = State()
    confirm_failed = State()