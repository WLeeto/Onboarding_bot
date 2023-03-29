
# todo Перенести всю эту дичь в БД и сделать админку для ее редактирования
# Mics -----------------------------------------------------------------------------------------------------------------
operator_list = [6126799078, ]  # Лист tg_id операторов
sleep_timer = 6  # Задержка перед удалением сообщения

# Messages -------------------------------------------------------------------------------------------------------------
greeting_message = "Добро пожаловать в команду ТИМ ФОРС! Я Тимур, бот для онбординга.\n" \
                   "У меня ты можешь узнать много полезной информации.\n" \
                   "https://teamforce.ru/"

newbie_greeting = "Потрясающе, в команде пополнение!\n" \
                  "Я бот {bot_name} Помогу тебе быстро адаптироваться в ТИМ ФОРС.\n" \
                  "Удели мне 7 минут За это время: \n" \
                  "- сформируем твою карточку специалиста \n" \
                  "- сориентирую, куда по каким вопросам обращаться \n" \
                  "- покажу волшебные кнопки, где храним важное.\n" \
                  "Самое время познакомиться. "

for_olds_message = "Привет! Я бот помощник Тимур. " \
                   "В ТИМ ФОРС много разных процессов, я создан помогать ориентироваться в рутинных вопросах. " \
                   "Микро план знакомства займет 3 минуты. " \
                   "Сначала давай проверим, знаешь ли ты о ТИМ ФОРС то, что знаю я?"

for_newbie_message = ""

we_are_closer_now = "Кажется мы стали чуточку ближе"

not_in_db = "Я не смог найти вас в БД. Вы у нас работаете ?"

message_dict = {
    "greetings": greeting_message,
    "greeting_video_id": "BAACAgIAAxkBAAILEWQAAXCXK-hny6PxMEFCsLjm50jwUwACBiYAAkLnAUhEeMXYd4w_7i4E",
    # BAACAgIAAxkBAAIEs2QS5x_ZNP-mVaEWYNfWcr2SXoB2AAK_KAACr3iYSOxofi9-8pdULwQ - для теста
    # BAACAgIAAxkBAAILEWQAAXCXK-hny6PxMEFCsLjm50jwUwACBiYAAkLnAUhEeMXYd4w_7i4E - для прода
    "for_olds_message": for_olds_message,
    "for_newbie_message": for_newbie_message,
    "we_are_closer_now": we_are_closer_now,
    "newbie_greeting": newbie_greeting,
    "not_in_db": not_in_db,
}

# Start_survey ---------------------------------------------------------------------------------------------------------
wana_start_yes_button = "Да, вперед !"
wana_start_no_button = "Нет, не сейчас"
wana_start_no_message = "Ну и ладно, а я старался, вопросы придумывал Т_Т"

first_question_text = "❔ Год основания ТИМ ФОРС? ❔"
first_question_answer_1 = "1996"
first_question_answer_2 = "2019"
first_question_answer_3 = "2008"
correct_first_answer = "2008"

second_question_text = "❔ Какой корпоративный цвет ТИМ ФОРС? ❔"
second_question_answer_1 = "Черный"
second_question_answer_2 = "Фиолетовый"
second_question_answer_3 = "Оранжевый"
correct_second_answer = "Оранжевый"

third_question_text = "❔ 'Бодрее' нужно говорить бодрее, а ... (продолжите фразу) ❔"
third_question_answer_1 = "'Громче'-громче"
third_question_answer_2 = "'Веселее'-веселее"
third_question_answer_3 = "'Четче'-четче"
correct_third_answer = "'Веселее'-веселее"

start_survey_dict = {
    "wana_start_yes_button": wana_start_yes_button,
    "wana_start_no_button": wana_start_no_button,

    "wana_start_no_message": wana_start_no_message,

    "first_question_text": first_question_text,
    "first_question_answer_1": first_question_answer_1,
    "first_question_answer_2": first_question_answer_2,
    "first_question_answer_3": first_question_answer_3,
    "correct_first_answer": correct_first_answer,

    "second_question_text": second_question_text,
    "second_question_answer_1": second_question_answer_1,
    "second_question_answer_2": second_question_answer_2,
    "second_question_answer_3": second_question_answer_3,
    "correct_second_answer": correct_second_answer,

    "third_question_text": third_question_text,
    "third_question_answer_1": third_question_answer_1,
    "third_question_answer_2": third_question_answer_2,
    "third_question_answer_3": third_question_answer_3,
    "correct_third_answer": correct_third_answer,
}

# Commands -------------------------------------------------------------------------------------------------------------

contacts = "<b>Какие контакты ищем?</b>"
contacts_hr = "<b>Отдел кадров</b> group_kdp@teamforce.ru"
contacts_contracts = "<b>Договорной отдел</b> group_contracts@teamforce.ru"
contacts_resourses = "<b>Ресурсный отдел</b> smartdev@teamforce.ru"

vacation = "Ежегодный оплачиваемый отпуск - 28 календарных дня в году\n\n" \
           "Чтобы взять отпуск следует:\n" \
           "- Согласовать сроки с руководителем проекта за 2 недели до желаемой даты\n" \
           "- Оформить заявление на отпуск и направить в кадровый отдел\n" \
           "- Проинформировать команду о предстоящем отпуске\n" \
           "- Поставить 'отбойник в почте' к кому обращаться по время отсутствия\n\n" \

docs = "Заглушка для команды <b>/docs</b>"

finance = "Правила выплаты заработной платы для штатников:\n" \
          "Работодатель выплачивает работникам заработную плату не реже чем два раза в месяц:\n" \
          "-20 (Двадцатого) числа каждого месяца выплачивается заработная плата за первую половину текущего месяца " \
          "из расчета фактически отработанного времени;\n" \
          "- 5 (Пятого) числа следующего месяца осуществляется окончательный расчет по итогам работы " \
          "за предыдущий месяц. При совпадении дня выплаты с выходным или нерабочим праздничным днем выплата " \
          "заработной платы производится накануне этого дня. Оплата производится пропорционально отработанному времени."

business_trip = "Вас отправляют в командироку?\n" \
                "Ознакомьтесь с положением о командировках и заполните следующие документы:\n" \

projects = "<b>Список проектов.</b>\n" \
           "Чтобы узнать подробнее, кликните по соответствующей кнопке:"

vacation_more_two_weeks = "<b> Давай я помогу тебе направить заявление на оплачиваемый отпуск.</b>\n\n" \
                          " Сначала убедись что ты сделал все из списка:\n" \
                          "1. Согласовал сроки с руководителем проекта за 2 недели до желаемой даты \n" \
                          "2. Проинформировал команду о предстоящем отпуске\n" \
                          "3. Поставил 'отбойник в почте' к кому обращаться по время отсутствия\n\n" \
                          " Если все из вышеперечисленного сделано, " \
                          "смело скачивай заявление и жми 'Подать заявку на отпуск':"

vacation_less_two_weeks = "<b>Если до отпуска меньше двух недель," \
                          " а заявление ты еще не подал то есть два варианта:</b>\n" \
                          "1. Оформить отпуск за свой счет\n" \
                          "2. Если до отпуска больше 4ех дней - максимально оперативно связаться с отделом кадров\n\n" \
                          " Вот тебе быстрые кнопочки чтобы взять отпуск за свой счет или связаться с отделом кадров:"

vacation_pay = "<b>Отпускние рассчитываются путем умножения среднедневного" \
               " заработка на количество календарных дней отпуска</b>\n" \
               "* Среднедневной заработок исчисляется путем деления " \
               "фактически начисленного дохода за расчетный период" \
               "на количество фактически отработанных дней в расчетном периоде \n" \
               "* Расчетным периодом считается календарный год, предшествующий началу отпуска\n" \
               "* Каждый полностью отработанный месяц " \
               "(когда рабочие дни по производственному календарю отработаны полностью) - составляет 29,3 дня\n" \
               "* Отпускные выплачиваются не позднее чем за 3 рабочих дня до начала отпуска"

vacation_more_two_weeks_not_state = "<b>Что нужно сделать:</b>\n" \
                                    "1. Согласовать сроки с руководителем проекта за 2 недели до желаемой даты\n" \
                                    "2. Проинформировать команду о предстоящем отпуске\n" \
                                    "3. Поставить 'отбойник в почте' к кому обращаться"

vacation_less_two_weeks_not_state = "Согласовать сроки с руководителем проекта"

about = "Не найден ответ по id 27"

commands_dict = {
    "contacts": contacts,
    "vacation": {
        "vacation": vacation,
        "vacation_more_two_weeks": vacation_more_two_weeks,
        "vacation_less_two_weeks": vacation_less_two_weeks,
        "vacation_more_two_weeks_not_state": vacation_more_two_weeks_not_state,
        "vacation_less_two_weeks_not_state": vacation_less_two_weeks_not_state,
        "vacation_pay": vacation_pay,
    },
    "docs": docs,
    "finance": finance,
    "bt": business_trip,
    "contacts_hr": contacts_hr,
    "contacts_contracts": contacts_contracts,
    "contacts_resourses": contacts_resourses,
    "projects": projects,
    "about": about,
}

# # Projects
# -------------------------------------------------------------------------------------------------------------
#
# B2BCloud = "Цифровая платформа B2BCloud(ссылка на сайт: https://smartstaffing.ru )" \
#            "для управления ИТ-проектами в крупных компаниях," \
#            " которая оцифровывает экосистему предоставления комплексных ИТ-услуг." \
#            " Осуществляет оценку, ресурсное моделирование и контроль ИТ-проектов," \
#            " управление ресурсным пулом внутренних и внешних специалистов." \
#            " В основе – межкорпоративная сеть на базе распределенных реестров," \
#            "где конечные клиенты эффективно взаимодействуют со своими партнерами для реализации ИТ-проектов, " \
#            "а сервисные ИТ-компании реализуют совместные клиентские проекты. " \
#            "На основе концепции СмартСтаффинг " \
#            "( ссылка:  https://drive.google.com/drive/folders/1fV9QmkUjYHnyFOJpzQkW_4wody8Frvlc)"
# Skils_Cloud = "Открытая структурированная площадка," \
#               "на которой специалисты могут опубликовать свои компетенции и вступить в оцифрованный пул," \
#               "из которого заказчики обеспечивают свои проекты ИТ-специалистами. " \
#               "Ссылка на сайт ( https://skillscloud.ru )"
# ONEC_ERP = "Заглушка. Описания нет"
# TF360 = "Мобильное приложение:\n\n" \
#         "Google Play: https://play.google.com/store/apps/details?id=com.teamforce.thanksapp\n" \
#         "RuStore: https://apps.rustore.ru/app/com.teamforce.thanksapp\n" \
#         "IOS:  https://testflight.apple.com/join/LhHajOy8\n\n" \
#         "Веб-платформа https://teamforce360.com\n\n" \
#         "Техподдержка (не смотрите что бот, за ним живые люди) https://t.me/TF360SupportBot\n\n" \
#         "Ваш рабочий тг кабинет https://t.me/DigitalRefBot\n\n" \
#         "Сайт проекта https://teamforce360.ru"
# Smart_Back_Office = "Интеллектуальное решение для оптимизации вспомогательных процессов в ИТ-компаниях," \
#                     "составляющих до 50% общего рабочего времени. " \
#                     "Используются нейросетевые технологии (NLP, NER, NLG) " \
#                     "и методы оценки неуверенности нейросетевых моделей."
# Hacker_Home = "Заглушка. Описания нет"
# Light = "Заглушка. Описания нет"
#
# project_dict = {
#     "B2BCloud": B2BCloud,
#     "Skils_Cloud": Skils_Cloud,
#     "1C_ERP": ONEC_ERP,
#     "TF360": TF360,
#     "Smart_Back_Office": Smart_Back_Office,
#     "Hacker_Home": Hacker_Home,
#     "Light": Light,
# }