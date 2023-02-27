# todo Перенести всю эту дичь в БД и сделать админку для ее редактирования
# Mics -----------------------------------------------------------------------------------------------------------------
operator_list = [6126799078, ]  # Лист tg_id операторов
sleep_timer = 6  # Задержка перед удалением сообщения


# Messages -------------------------------------------------------------------------------------------------------------
greeting_message = "Приходит приветственное сообщение о начале использования бота"

newbie_greeting = "Потрясающе, в команде пополнение!\n" \
                  "Я бот {bot_name} Помогу тебе быстро адаптироваться в ТИМ ФОРС.\n" \
                  "Удели мне 7 минут За это время: \n" \
                  "- сформируем твою карточку специалиста \n" \
                  "- сориентирую, куда по каким вопросам обращаться \n" \
                  "- покажу волшебные кнопки, где храним важное.\n" \
                  "Самое время познакомиться. "

help_message = "В моём меню хранятся полезные команды. \n" \
               "Чтобы воспользоваться, просто надо нажать на интересующую и следовать моим подсказкам: \n" \
               "/find - помогу найти сотрудника"

for_olds_message = "Привет! Я бот помощник ХХХХ. " \
                   "В ТИМ ФОРС много разных процессов, я создан помогать ориентироваться в рутинных вопросах. " \
                   "Микро план знакомства займет 3 минуты. " \
                   "Сначала давай проверим, знаешь ли ты о ТИМ ФОРС то, что знаю я?"

for_newbie_message = ""

we_are_closer_now = "Кажется мы стали чуточку ближе"

message_dict = {
    "greetings": greeting_message,
    "help": help_message,
    "greeting_video_id": "BAACAgIAAxkBAAICZGP2BZ7w694CN-2LtEQRbeq7XJetAAIIJwACV--wS1rJTQijj4V0LgQ",
    "for_olds_message": for_olds_message,
    "for_newbie_message": for_newbie_message,
    "we_are_closer_now": we_are_closer_now,
    "newbie_greeting": newbie_greeting,
}

# Start_survey ---------------------------------------------------------------------------------------------------------
wana_start_yes_button = "Да, вываливай !"
wana_start_no_button = "Нет, надоели тесты Т_Т"
wana_start_no_message = "Ну и ладно, а я старался, вопросы придумывал Т_Т"

first_question_text = "❔ Чем должен заниматься ночью уважающий себя кот? ❔"
first_question_answer_1 = "Тыгыдыкать"
first_question_answer_2 = "Орать"
first_question_answer_3 = "Шуршать"
correct_first_answer = "Тыгыдыкать"

second_question_text = "❔ Что является национальным животным Шотландии? ❔"
second_question_answer_1 = "Лошадь"
second_question_answer_2 = "Единорог"
second_question_answer_3 = "Корова"
correct_second_answer = "Единорог"

third_question_text = "❔ Какая страна производит больше всего кофе в мире? ❔"
third_question_answer_1 = "Колумбия"
third_question_answer_2 = "Индонезия"
third_question_answer_3 = "Бразилия"
correct_third_answer = "Бразилия"

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
