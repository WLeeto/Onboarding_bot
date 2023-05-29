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
    save_department = State()
    save_type_of_employement = State()
    save_first_working_day = State()
    confirm_failed = State()
    change_name = State()
    change_bday = State()
    change_phone = State()
    change_email = State()
    change_hobbie = State()
    procced = State()

    edit_hobbie = State()
    edit_job = State()
    edit_email = State()
    schedulered_card_step_1 = State()

    step_1 = State()
    step_2 = State()
    step_3 = State()
    step_4 = State()
    step_5 = State()
    step_6 = State()
    step_7 = State()
    step_8 = State()
    step_9 = State()
    step_10 = State()
    step_11 = State()
    step_12 = State()
    step_13 = State()
    step_14 = State()
    step_15 = State()
    step_16 = State()
    step_17 = State()
    step_18 = State()
    step_19 = State()
    step_20 = State()
    step_21 = State()
    step_22 = State()
    step_23 = State()
    step_24 = State()
    step_25 = State()
    step_26 = State()
    step_27 = State()
    step_28 = State()
    commit_data_email = State()

    other = State()

    finish = State()


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


class FSM_scheldule_test(StatesGroup):
    start = State()


class FSM_send_vacation_email(StatesGroup):
    enter_vacation_period = State()
    is_agreed = State()
    send_doc = State()
    enter_coordinator = State()
    commit_data = State()
    # what_type_of_employement = State()


class FSM_search(StatesGroup):
    enter_name = State()
    enter_surname = State()
    enter_patronymic = State()
    enter_email = State()
    enter_tg_nickname = State()
    enter_department = State()
    enter_title = State()
    enter_phone = State()


class FSM_newbie_xlsx(StatesGroup):
    step_1 = State()
    step_2 = State()
    step_3 = State()
    step_4 = State()
    step_5 = State()
    step_6 = State()
    step_7 = State()
    step_8 = State()
    step_9 = State()
    step_10 = State()
    step_11 = State()
    step_12 = State()
    step_13 = State()
    step_14 = State()
    step_15 = State()
    step_16 = State()
    step_17 = State()
    step_18 = State()
    step_19 = State()
    step_20 = State()
    step_21 = State()
    step_22 = State()
    step_23 = State()
    step_24 = State()
    step_25 = State()
    step_26 = State()
    step_27 = State()
    step_28 = State()
    commit_data = State()

    other = State()

    finish = State()


class FSM_button_paginator(StatesGroup):
    button_paginator = State()

