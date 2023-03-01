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

help_message = "В моём меню хранятся полезные команды. \n" \
               "/benefits - Информация о бонусах\n" \
               "/business_trip - Подготовка к командировке\n" \
               "/contacts - Контакты всех отделов\n" \
               "/docs - Выводит чеклист, что требуется для оформления\n" \
               "/find - Поиск контактных данных сотрудников\n" \
               "/finance - Вопросы по перечислениям\n" \
               "/initiative - Сбор инициатив/идей и предложений\n" \
               "/office - Информация про адрес\n" \
               "/vacation - Подготовка к отпуску\n" \
               "/referal - Информация о реферальной программе\n" \
               "/tf360 - О проекте ТФ360" \
               "/social_media - Ссылки на наши соцсети\n" \
               "/support - Помогает найти ответственного по вопросу\n" \


for_olds_message = "Привет! Я бот помощник Тимур. " \
                   "В ТИМ ФОРС много разных процессов, я создан помогать ориентироваться в рутинных вопросах. " \
                   "Микро план знакомства займет 3 минуты. " \
                   "Сначала давай проверим, знаешь ли ты о ТИМ ФОРС то, что знаю я?"

for_newbie_message = ""

we_are_closer_now = "Кажется мы стали чуточку ближе"

message_dict = {
    "greetings": greeting_message,
    "help": help_message,
    "greeting_video_id": "BAACAgIAAxkBAAIJa2P_J6XH2_qBoq2UXfr6Seuy3zoQAAIjKQACOz34S8bdO_PujPlyLgQ",
    "for_olds_message": for_olds_message,
    "for_newbie_message": for_newbie_message,
    "we_are_closer_now": we_are_closer_now,
    "newbie_greeting": newbie_greeting,
}

# Start_survey ---------------------------------------------------------------------------------------------------------
wana_start_yes_button = "Да, пройду тест"
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

contacts = "<b>Отдел кадров</b> group_kdp@teamforce.ru\n" \
           "Распространенные обращения:\n" \
           "- оформление отпуска\n" \
           "- информирование о больничном\n" \
           "- запросы расчетных листков\n" \
           "- подписание трудовых договоров\n\n" \
           "<b>Договорной отдел</b> group_contracts@teamforce.ru\n" \
           "Распространенные вопросы:\n" \
           "- согласование договоров на работы\n" \
           "- уточнение вопросов по оплатам\n\n" \
           "<b>Ресурсный отдел</b> smartdev@teamforce.ru\n" \
           "Распространенные вопросы:\n" \
           "- уточнение свободных вакансий для друзей "

vacation = "Заглушка для команды <b>/vacation</b>"

benefits = "Рады представить Вам бенефит-кафе - привилегии для сотрудников ТИМ ФОРС.\n" \
           "Из бенефит-кафе, раз в год Вы можете выбрать один* понравившийся бенефит из предложенного " \
           "'меню'(здоровье, образование, путешествия и досуг) на определенную сумму**\n\n" \
           "*Неиспользованный за год бенефит, сгорает.\n" \
           "**Ваучер на сумму 23 000 рублей(получить наличными его нельзя) с возможностью выставления счета на ЮЛ.\n\n" \
           "Для получения дополнительной информации, просьба обращаться к @vkim_teamforce"

docs = "Заглушка для команды <b>/docs</b>"

referal = "Заглушка для команды <b>/referal</b>"

tf360 = "Заглушка для команды <b>/tf360</b>"

support = "<b>У Вас остались вопросы?</b>\n" \
          "Расскажите мне, что Вас интересует?\n" \
          "@vkim_teamforce"

social_media = "<b>Подробнее о компании Вы можете узнать на сайтах:</b>\n" \
               "https://smartstaffing.ru\n" \
               "https://teamforce.ru/\n" \
               "https://teamforce.ru/welcomebook/\n" \
               "https://tatmobile.solutions/\n\n" \
               "Подписывайтесь и следите за нашими новостями!\n" \
               "https://vk.com/teamforcex\n" \
               "https://t.me/teamforcex\n" \
               "https://instagram.com/teamforce.ru\n" \
               "https://www.facebook.com/teamforceX"

initiative = "Проводим сбор инициатив/идей и предложений"

finance = "Заглушка для команды <b>/finance</b>"

office = "<b>Как к нам попасть:</b>\n" \
         "Территория Инновационного центра 'Сколково'\n" \
         "д. Сколково, Большой бульвар, д.42, стр. 1, офис 337, ядро 4"

business_trip = "Вас отправляют в командироку?\n" \
                "Ознакомьтесь с положением о командировках и заполните следующие документы:\n" \

commands_dict = {
    "contacts": contacts,
    "vacation": vacation,
    "benefits": benefits,
    "docs": docs,
    "support": support,
    "social_media": social_media,
    "initiative": initiative,
    "finance": finance,
    "office": office,
    "business_trip": business_trip,
    "referal": referal,
    "tf360": tf360,
}
