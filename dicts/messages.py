from create_bot import db

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
               "/find - Поиск контактных данных сотрудников\n" \
               "/finance - Вопросы по перечислениям\n" \
               "/initiative - Сбор инициатив/идей и предложений\n" \
               "/office - Информация про адрес\n" \
               "/vacation - Подготовка к отпуску\n" \
               "/referal - Информация о реферальной программе\n" \
               "/tf360 - О проекте ТФ360" \
               "/social_media - Ссылки на наши соцсети\n" \
               "/support - Помогает найти ответственного по вопросу\n" \
               "/social_media - Мы в соцсетях" \


for_olds_message = "Привет! Я бот помощник Тимур. " \
                   "В ТИМ ФОРС много разных процессов, я создан помогать ориентироваться в рутинных вопросах. " \
                   "Микро план знакомства займет 3 минуты. " \
                   "Сначала давай проверим, знаешь ли ты о ТИМ ФОРС то, что знаю я?"

for_newbie_message = ""

we_are_closer_now = "Кажется мы стали чуточку ближе"

message_dict = {
    "greetings": greeting_message,
    "help": help_message,
    "greeting_video_id": "BAACAgIAAxkBAAILEWQAAXCXK-hny6PxMEFCsLjm50jwUwACBiYAAkLnAUhEeMXYd4w_7i4E",
    "for_olds_message": for_olds_message,
    "for_newbie_message": for_newbie_message,
    "we_are_closer_now": we_are_closer_now,
    "newbie_greeting": newbie_greeting,
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

vacation = "Чтобы взять отпуск следует:\n" \
           "- Согласовать сроки с руководителем проекта за 2 недели до желаемой даты\n" \
           "- Оформить заявление на отпуск и направить в кадровый отдел\n" \
           "- Проинформировать команду о предстоящем отпуске\n" \
           "- Поставить 'отбойник в почте' к кому обращаться по время отсутствия\n\n" \

benefits = "Рады представить Вам бенефит-кафе - привилегии для сотрудников ТИМ ФОРС.\n" \
           "Из бенефит-кафе, раз в год Вы можете выбрать один* понравившийся бенефит из предложенного " \
           "'меню'(здоровье, образование, путешествия и досуг) на определенную сумму**\n\n" \
           "*Неиспользованный за год бенефит, сгорает.\n" \
           "**Ваучер на сумму 23 000 рублей(получить наличными его нельзя) с возможностью выставления счета на ЮЛ.\n\n" \
           "Для получения дополнительной информации, просьба обращаться к @vkim_teamforce"

docs = "Заглушка для команды <b>/docs</b>"

referal = "Team Force активно растет и развивается" \
          " и с каждым днем возрастает необходимость закрывать как можно больше позиций " \
          "эффективными и лояльными сотрудниками как внутри компании, так и для наших заказчиков.\n" \
          "Поэтому мы приняли решение дать Вам возможность рассказать о своих знакомых, " \
          "которые находятся в поиске работы или Вы хотели бы работать вместе, " \
          "но не знаете какие у нас есть вакансии.\n\n" \
          "У нас действует реферальная программа — Team Force Referrals.\n" \
          "Суть программы — вы рекомендуете нам своих друзей и знакомых, " \
          "в случае их трудоустройства получаете привлекательный бонус:\n\n" \
          "Для того, чтобы рекомендовать кандидата необходимо отправить резюме на почту Cv@teamforce.ru.\n" \
          "Премия выплачивается вам после прохождения рефералом испытательного срока 3 месяца " \
          "или 1 месяц в случае оформления по ИП. Срок действия программы до 31.12.2023"

tf360 = "Мобильное приложение:\n" \
        "Google Play: https://play.google.com/store/apps/details?id=com.teamforce.thanksapp\n" \
        "RuStore: https://apps.rustore.ru/app/com.teamforce.thanksapp\n" \
        "IOS: https://testflight.apple.com/join/LhHajOy8\n\n" \
        "Веб-платформа https://teamforce360.com\n" \
        "Техподдержка (не смотрите что бот, за ним живые люди) https://t.me/TF360SupportBot\n" \
        "Ваш рабочий тг кабинет https://t.me/DigitalRefBot\n" \
        "Сайт проекта https://teamforce360.ru"

support = "<b>У Вас остались вопросы?</b>\n" \
          "Расскажите мне, что Вас интересует?\n" \
          "@vkim_teamforce"

social_media = "<b>Подробнее о компании Вы можете узнать на сайтах:</b>\n" \
               "<a href='https://smartstaffing.ru'>СмартСтаффинг</a>\n" \
               "<a href='https://teamforce.ru/'>ТИМ ФОРС</a>\n" \
               "<a href='https://teamforce.ru/welcomebook/'>Велкомбук ТИМ ФОРС</a>\n" \
               "<a href='https://tatmobile.solutions/'>ТатМобайлИнформСиДиСи</a>\n\n" \
               "<b>Подписывайтесь и следите за нашими новостями!</b>\n" \
               "<a href='https://vk.com/teamforcex'>Вконтакте</a>\n" \
               "<a href='https://t.me/teamforcex'>Telegram</a>\n" \
               "<a href='https://instagram.com/teamforce.ru'>Instagram</a>\n" \
               "<a href='https://www.facebook.com/teamforceX'>Facebook</a>"

initiative = "Проводим сбор инициатив/идей и предложений"

finance = "Правила выплаты заработной платы для штатников:\n" \
          "Работодатель выплачивает работникам заработную плату не реже чем два раза в месяц:\n" \
          "-20 (Двадцатого) числа каждого месяца выплачивается заработная плата за первую половину текущего месяца " \
          "из расчета фактически отработанного времени;\n" \
          "- 5 (Пятого) числа следующего месяца осуществляется окончательный расчет по итогам работы " \
          "за предыдущий месяц. При совпадении дня выплаты с выходным или нерабочим праздничным днем выплата " \
          "заработной платы производится накануне этого дня. Оплата производится пропорционально отработанному времени."

office = "<b>Как к нам попасть:</b>\n" \
         "Территория Инновационного центра 'Сколково'\n" \
         "д. Сколково, Большой бульвар, д.42, стр. 1, офис 337, ядро 4\n" \
         "(видео: https://disk.yandex.ru/i/v2GaULdsHJyCLg)\n\n" \
         "По ссылке Вы можете увидеть карту проезда и схему парковок: https://sk.ru/transport/"

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
               "(когда рабочие дни по производственному календарю отработаны полностью) - составляет 29,3 дня"

vacation_more_two_weeks_not_state = "<b>Что нужно сделать:</b>\n" \
                                    "1. Согласовать сроки с руководителем проекта за 2 недели до желаемой даты\n" \
                                    "2. Проинформировать команду о предстоящем отпуске\n" \
                                    "3. Поставить 'отбойник в почте' к кому обращаться"

vacation_less_two_weeks_not_state = "Согласовать сроки с руководителем проекта"

about = db.find_answer_by_answer_id(27).answer_text if db.find_answer_by_answer_id(27) else "Не найден ответ по id 27"

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
    "contacts_hr": contacts_hr,
    "contacts_contracts": contacts_contracts,
    "contacts_resourses": contacts_resourses,
    "projects": projects,
    "about": about,
}

# Projects -------------------------------------------------------------------------------------------------------------

B2BCloud = "Цифровая платформа B2BCloud ( ссылка на сайт: https://smartstaffing.ru )" \
           "для управления ИТ-проектами в крупных компаниях," \
           " которая оцифровывает экосистему предоставления комплексных ИТ-услуг." \
           " Осуществляет оценку, ресурсное моделирование и контроль ИТ-проектов," \
           " управление ресурсным пулом внутренних и внешних специалистов." \
           " В основе – межкорпоративная сеть на базе распределенных реестров, " \
           "где конечные клиенты эффективно взаимодействуют со своими партнерами для реализации ИТ-проектов, " \
           "а сервисные ИТ-компании реализуют совместные клиентские проекты. " \
           "На основе концепции СмартСтаффинг " \
           "( ссылка:  https://drive.google.com/drive/folders/1fV9QmkUjYHnyFOJpzQkW_4wody8Frvlc )"
Skils_Cloud = "Открытая структурированная площадка, " \
              "на которой специалисты могут опубликовать свои компетенции и вступить в оцифрованный пул, " \
              "из которого заказчики обеспечивают свои проекты ИТ-специалистами. " \
              "Ссылка на сайт ( https://skillscloud.ru )"
ONEC_ERP = "Заглушка. Описания нет"
TF360 = "Мобильное приложение:\n\n" \
        "Google Play: https://play.google.com/store/apps/details?id=com.teamforce.thanksapp\n" \
        "RuStore: https://apps.rustore.ru/app/com.teamforce.thanksapp\n" \
        "IOS:  https://testflight.apple.com/join/LhHajOy8\n\n" \
        "Веб-платформа https://teamforce360.com\n\n" \
        "Техподдержка (не смотрите что бот, за ним живые люди) https://t.me/TF360SupportBot\n\n" \
        "Ваш рабочий тг кабинет https://t.me/DigitalRefBot\n\n" \
        "Сайт проекта https://teamforce360.ru"
Smart_Back_Office = "Интеллектуальное решение для оптимизации вспомогательных процессов в ИТ-компаниях, " \
                    "составляющих до 50% общего рабочего времени. " \
                    "Используются нейросетевые технологии (NLP, NER, NLG) " \
                    "и методы оценки неуверенности нейросетевых моделей."
Hacker_Home = "Заглушка. Описания нет"
Light = "Заглушка. Описания нет"

project_dict = {
    "B2BCloud": B2BCloud,
    "Skils_Cloud": Skils_Cloud,
    "1C_ERP": ONEC_ERP,
    "TF360": TF360,
    "Smart_Back_Office": Smart_Back_Office,
    "Hacker_Home": Hacker_Home,
    "Light": Light,
}