# todo Перенести всю эту дичь в БД и сделать админку для ее редактирования
# Mics -----------------------------------------------------------------------------------------------------------------
from os import environ

# operator_list = [6126799078, ]  # Я оператор
operator_list = [980900767, ]  # Виолетта оператор
testers_list = [5148438149, ]
administarator_list = [5148438149, 148785954, 458926263, 843059374, 1376939445, 1341062023, 5120778705, 302337090, ]
sleep_timer = 6  # Задержка перед удалением сообщения

# Messages -------------------------------------------------------------------------------------------------------------
greeting_message = "Добро пожаловать в команду ТИМ ФОРС! Я Тимур, бот для онбординга.\n" \
                   "У меня ты можешь узнать много полезной информации.\n" \

newbie_greeting = "Потрясающе, в команде пополнение✨\n" \
                  "Добро пожаловать в команду ТИМ ФОРС!\n" \
                  "Я Тимур, бот для онбординга @onboardingtfbot, " \
                  "помогу тебе быстро адаптироваться в ТИМ ФОРС (https://teamforce.ru/). " \
                  "У меня ты можешь узнать много полезной информации😇\n\n" \
                  "📌Уделишь мне 7 минут? За это время я:\n" \
                  "- Сформирую твою карточку специалиста\n" \
                  "- Сориентирую, куда и по каким вопросам обращаться\n" \
                  "- Покажу волшебные кнопки, где храним важное\n\n" \
                  "Самое время познакомиться!"

for_olds_message = "Привет! Я бот помощник Тимур. " \
                   "В ТИМ ФОРС много разных процессов, я создан помогать ориентироваться в рутинных вопросах. " \
                   "Микроплан знакомства займет 3 минуты. " \
                   "Сначала давай проверим, знаешь ли ты о ТИМ ФОРС то, что знаю я?"

for_newbie_message = ""

we_are_closer_now = "Кажется, мы стали чуточку ближе 😇"

not_in_db = "Я не смог найти вас в БД. Передайте свой tg_id администратору, он вас добавит ^_^"

start_not_in_db = "Привет, друг\! Я Тимур, бот для онбординга @onboardingtfbot, " \
                  "помогу тебе быстро адаптироваться в **[ТИМ ФОРС](https://teamforce.ru)** \. " \
                  "У меня ты можешь узнать много полезной информации😇\n\n" \
                  "К сожалению, я не нашел тебя в своей базе\. Пожалуйста, обратись к \@vkim\_teamforce\n" \
                  "Скорее всего нужно будет передать свой id: `{tgid}`\n" \
                  "Чтобы заново запустить бота, вводи команду /start\n\n" \
                  "До скорых встреч\!"

help_message = "/contacts - Контакты всех отделов\n" \
               "/vacation - Подготовка к отпуску\n" \
               "/benefits - Информация о бонусах компании и о способах получения\n" \
               "/support - Помогает найти ответственного по вопросу\n" \
               "/social_media - Ссылки на наши соцсети\n" \
               "/initiative - Сбор инициатив/идей и предложений\n" \
               "/finance - Вопросы по перечислениям\n" \
               "/bt - Подготовка к командировке\n" \
               "/find - Поиск контактных данных по фио, должности\n" \
               "/referal - Информация о реферальной программе\n" \
               "/office - Информация про офис\n" \
               "/tf360 - О проекте ТИМФОРС360.Цифровое спасибо\n" \
               "/projects - Краткая информация о проектах\n" \
               "/about - Информация о ТИМ ФОРС\n" \
               "/sick_leave - Информация о больничном\n"

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
    "start_not_in_db": start_not_in_db,
    "help_message": help_message,
}

# Start_survey ---------------------------------------------------------------------------------------------------------
wana_start_yes_button = "Да, вперед!"
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
