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


class FSM_business_trip_form_sending(StatesGroup):
    start_business_trip_form = State()
    enter_dates = State()
    save_note = State()
    save_advance = State()
    save_tickets = State()
    save_checks = State()
    send_form = State()


class FSM_type_of_employment(StatesGroup):
    change_type_of_employment = State()


class FSM_meeting(StatesGroup):
    start = State()
    step_2 = State()
    step_3 = State()
    end = State()