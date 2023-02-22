# todo Перенести всю эту дичь в БД и сделать админку для ее редактирования
# Messages -------------------------------------------------------------------------------------------------------------
greeting_message = "Приходит приветственное сообщение о начале использования бота и видео"

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
}

# Start_survey ---------------------------------------------------------------------------------------------------------
wana_start_yes_button = "Да, вываливай !"
wana_start_no_button = "Нет, надоели тесты Т_Т"
wana_start_no_message = "Ну и ладно, а я старался, вопросы придумывал Т_Т"

first_question_text = "first_question_text"
first_question_answer_1 = "first_question_answer_1"
first_question_answer_2 = "first_question_answer_2"
first_question_answer_3 = "first_question_answer_3"

second_question_text = "second_question_text"
second_question_answer_1 = "second_question_answer_1"
second_question_answer_2 = "second_question_answer_2"
second_question_answer_3 = "second_question_answer_3"

third_question_text = "third_question_text"
third_question_answer_1 = "third_question_answer_1"
third_question_answer_2 = "third_question_answer_2"
third_question_answer_3 = "third_question_answer_3"

start_survey_dict = {
    "wana_start_yes_button": wana_start_yes_button,
    "wana_start_no_button": wana_start_no_button,

    "wana_start_no_message": wana_start_no_message,

    "first_question_text": first_question_text,
    "first_question_answer_1": first_question_answer_1,
    "first_question_answer_2": first_question_answer_2,
    "first_question_answer_3": first_question_answer_3,

    "second_question_text": second_question_text,
    "second_question_answer_1": second_question_answer_1,
    "second_question_answer_2": second_question_answer_2,
    "second_question_answer_3": second_question_answer_3,

    "third_question_text": third_question_text,
    "third_question_answer_1": third_question_answer_1,
    "third_question_answer_2": third_question_answer_2,
    "third_question_answer_3": third_question_answer_3,
}


sleep_timer = 6  # Задержка перед удалением сообщения