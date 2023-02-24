from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dicts.messages import start_survey_dict

"""
Клавиатура для старта приветственного опроса
"""


class Survey_inlines_keyboards:
    def __init__(self, rows_in_line=1):
        self.rows_in_line = rows_in_line

        self.survey_text_yes = start_survey_dict["wana_start_yes_button"]
        self.survey_text_no = start_survey_dict["wana_start_no_button"]

        self.first_question_answer_1 = start_survey_dict["first_question_answer_1"]
        self.first_question_answer_2 = start_survey_dict["first_question_answer_2"]
        self.first_question_answer_3 = start_survey_dict["first_question_answer_3"]

        self.second_question_answer_1 = start_survey_dict["second_question_answer_1"]
        self.second_question_answer_2 = start_survey_dict["second_question_answer_2"]
        self.second_question_answer_3 = start_survey_dict["second_question_answer_3"]

        self.third_question_answer_1 = start_survey_dict["third_question_answer_1"]
        self.third_question_answer_2 = start_survey_dict["third_question_answer_2"]
        self.third_question_answer_3 = start_survey_dict["third_question_answer_3"]

    def start_survey(self):
        start_survey = InlineKeyboardMarkup(row_width=self.rows_in_line)
        button_1 = InlineKeyboardButton(text=self.survey_text_yes, callback_data="survey yes")
        button_2 = InlineKeyboardButton(text=self.survey_text_no, callback_data="survey no")
        start_survey.add(button_1, button_2)
        return start_survey

    def first_question(self):
        first_question = InlineKeyboardMarkup(row_width=self.rows_in_line)
        button_1 = InlineKeyboardButton(text=self.first_question_answer_1,
                                        callback_data="first" + " " + self.first_question_answer_1)
        button_2 = InlineKeyboardButton(text=self.first_question_answer_2,
                                        callback_data="first" + " " + self.first_question_answer_2)
        button_3 = InlineKeyboardButton(text=self.first_question_answer_3,
                                        callback_data="first" + " " + self.first_question_answer_3)
        first_question.add(button_1, button_2, button_3)
        return first_question

    def second_question(self):
        first_question = InlineKeyboardMarkup(row_width=self.rows_in_line)
        button_1 = InlineKeyboardButton(text=self.second_question_answer_1,
                                        callback_data="second" + " " + self.second_question_answer_1)
        button_2 = InlineKeyboardButton(text=self.second_question_answer_2,
                                        callback_data="second" + " " + self.second_question_answer_2)
        button_3 = InlineKeyboardButton(text=self.second_question_answer_3,
                                        callback_data="second" + " " + self.second_question_answer_3)
        first_question.add(button_1, button_2, button_3)
        return first_question

    def third_question(self):
        first_question = InlineKeyboardMarkup(row_width=self.rows_in_line)
        button_1 = InlineKeyboardButton(text=self.third_question_answer_1,
                                        callback_data="third" + " " + self.third_question_answer_1)
        button_2 = InlineKeyboardButton(text=self.third_question_answer_2,
                                        callback_data="third" + " " + self.third_question_answer_2)
        button_3 = InlineKeyboardButton(text=self.third_question_answer_3,
                                        callback_data="third" + " " + self.third_question_answer_3)
        first_question.add(button_1, button_2, button_3)
        return first_question




