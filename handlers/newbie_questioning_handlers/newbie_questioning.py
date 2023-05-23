import os

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import WrongFileIdentifier, CantInitiateConversation
from transliterate import translit

from States.states import FSM_newbie_questioning
from create_bot import bot, dp, db
from dicts.messages import message_dict, operator_list
from func.all_func import validate_email, validate_phone, validate_bday, is_latin
from keyboards.inline_newbie_questioning import change_newbie_questioning, back_to_name_kb, back_to_bdate_kb, \
    back_to_phone_kb, back_to_email_kb
from keyboards.inline_operator import confirm_new_user
from keyboards.inline_start_survey import Survey_inlines_keyboards


# @dp.callback_query_handler(lambda c: c.data == "start",
#                            state=FSM_newbie_questioning.newbie_questioning_start)
async def questioning_start(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    msg_todel = await callback_query.message.answer("Введи свое ФИО (Например: Пупкин Иван Александрович):")
    async with state.proxy() as data:
        data["to_delete"] = msg_todel
    await FSM_newbie_questioning.next()


# @dp.message_handler(state=FSM_newbie_questioning.asking_surname)
async def load_surname(message: types.Message, state: FSMContext):
    await message.delete()
    try:
        name = message.text.split(" ")[1]
        surname = message.text.split(" ")[0]
        patronymic = message.text.split(" ")[2]
        if is_latin(message.text):
            await FSM_newbie_questioning.next()
            keyboard = Survey_inlines_keyboards()
            async with state.proxy() as data:
                await data["to_delete"].edit_text("Я правильно написал твою фамилию на английском?:\n"
                                                  f"<b>{translit(surname, language_code='ru', reversed=True)}</b>\n"
                                                  "Эта формулировка будет использована в создании почты",
                                                  parse_mode="html",
                                                  reply_markup=keyboard.is_ok())
            async with state.proxy() as data:
                data["name"] = name
                data["patronymic"] = patronymic
                data["surname"] = surname
                data["tg_id"] = message.from_id
                data["tg_name"] = message.from_user.username
        else:
            async with state.proxy() as data:
                await data["to_delete"].edit_text("Пожалуйста, введи свое ФИО на кириллице")
    except IndexError:
        async with state.proxy() as data:
            await data["to_delete"].edit_text("Необходимо ввести фамилию, имя и отчество, три слова через пробел.\n"
                                              "Введи свое ФИО (Например: Пупкин Иван Александрович):")


# @dp.callback_query_handler(lambda c: c.data.startswith("answer"),
#                            state=FSM_newbie_questioning.email_creating)
async def email_confirming(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data.split(" ")[1] == "correct":
        async with state.proxy() as data:
            data["surname_eng"] = translit(data["surname"], language_code='ru', reversed=True)
            await data["to_delete"].edit_text("Введи свою дату рождения (формат dd.mm.yyyy): ",
                                              reply_markup=back_to_name_kb)
        await FSM_newbie_questioning.asking_bday.set()
    else:
        await FSM_newbie_questioning.asking_surname_eng.set()
        async with state.proxy() as data:
            await data["to_delete"].edit_text("Ок, тогда введи фамилию на английском:")


# @dp.message_handler(state=FSM_newbie_questioning.asking_surname_eng)
async def load_eng_surname(message: types.Message, state: FSMContext):
    await message.delete()
    await FSM_newbie_questioning.next()
    async with state.proxy() as data:
        data["surname_eng"] = message.text
        await data["to_delete"].edit_text("Введи свою дату рождения (формат dd.mm.yyyy): ",
                                          reply_markup=back_to_name_kb)


# @dp.message_handler(state=FSM_newbie_questioning.asking_bday)
async def load_bdate(message: types.Message, state: FSMContext):
    await message.delete()
    validator = validate_bday(message.text)
    if validator:
        await FSM_newbie_questioning.next()
        async with state.proxy() as data:
            data["bdate"] = validator
            await data["to_delete"].edit_text("Теперь введи свой телефон для связи (формат 7 ХХХ ХХХ ХХХХ): ",
                                              reply_markup=back_to_bdate_kb)

    else:
        async with state.proxy() as data:
            await data["to_delete"].edit_text("Необходимо ввести дату в формате dd.mm.yyyy\n"
                                              "(Например 28.07.1989)\n"
                                              "Дата должна быть минимум на 15 лет младше текущей")


# @dp.message_handler(state=FSM_newbie_questioning.asking_phone)
async def load_phone(message: types.Message, state: FSMContext):
    await message.delete()
    validator = validate_phone(message.text)
    if validator:
        await FSM_newbie_questioning.next()
        async with state.proxy() as data:
            data["phone"] = validator
            await data["to_delete"].edit_text("Укажи свой e-mail (для отправки документов): ",
                                              reply_markup=back_to_phone_kb)
    else:
        async with state.proxy() as data:
            await data["to_delete"].edit_text("Необходимо ввести телефон в формате 7 ХХХ ХХХ ХХХХ\n"
                                              "Например 7 917 233 4567")


# @dp.message_handler(state=FSM_newbie_questioning.asking_email)
async def load_email(message: types.Message, state: FSMContext):
    await message.delete()
    validator = validate_email(message.text)
    if validator:
        await FSM_newbie_questioning.next()
        async with state.proxy() as data:
            data["email"] = message.text
            await data["to_delete"].edit_text("Загрузи свое фото через скрепку 📎. "
                                              "Фотография будет использоваться в твоей карточке и опубликована "
                                              "в общем чате. "
                                              "Будет отлично, если она будет в деловом стиле.",
                                              reply_markup=back_to_email_kb)
    else:
        async with state.proxy() as data:
            await data["to_delete"].edit_text("Почта введена некорректно.\n"
                                              "Введите корректную почту:")


# @dp.message_handler(content_types="photo", state=FSM_newbie_questioning.asking_photo)
async def load_photo(message: types.Message, state: FSMContext):
    await message.delete()
    await FSM_newbie_questioning.next()
    destination = message.photo[-1].file_id
    async with state.proxy() as data:
        data["tg_photo_path"] = destination
        data["photo"] = message.photo[-1].file_id
        await data["to_delete"].edit_text("Расскажи о своих хобби и увлечениях. "
                                          "Чем любишь заниматься в свободное время? Что тебя вдохновляет и дает "
                                          "энергию?\n "
                                          "Пиши о себе все, чем ты хочешь поделиться с коллегами! "
                                          "Так будет быстрее найти единомышленников и друзей😊")


# @dp.message_handler(state=FSM_newbie_questioning.asking_photo)
async def waiting_for_photo(message: types.Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        await data["to_delete"].edit_text("Загрузи свое фото через скрепку 📎. "
                                          "Фотография будет использоваться в твоей карточке и "
                                          "опубликована в общем чате. "
                                          "Будет отлично, если она будет в деловом стиле.")


# @dp.message_handler(state=FSM_newbie_questioning.asking_hobby)
async def load_hobby(message: types.Message, state: FSMContext):
    await message.delete()
    keyboard = Survey_inlines_keyboards()
    async with state.proxy() as data:
        data["hobby"] = message.text
    await FSM_newbie_questioning.next()
    await message.answer_photo(data["photo"], 'Проверим, что получилось:\n\n'
                                              f'{data["surname"]} {data["name"]} {data["patronymic"]}\n'
                                              f'Дата рождения: {data["bdate"].strftime("%d.%m.%Y")}\n'
                                              f'Телефон: +{data["phone"]}\n'
                                              f'E-mail: {data["email"]}\n'
                                              f'Хобби и увлечения: {data["hobby"]}')
    buttons_to_remove = await message.answer("Все верно?", reply_markup=keyboard.is_ok())
    async with state.proxy() as data:
        data["buttons_to_remove"] = buttons_to_remove.message_id
        data["to_delete"] = []


# @dp.callback_query_handler(lambda c: c.data.startswith("answer"), state=FSM_newbie_questioning.commit_data)
async def commit_data(callback_query: types.CallbackQuery, state: FSMContext):
    keyboard = Survey_inlines_keyboards()
    if callback_query.data.split(" ")[1] == "correct":
        async with state.proxy() as data:
            db.add_newbie_for_confirming(
                tg_id=data["tg_id"],
                first_name=data["name"],
                surname=data["surname"],
                middle_name=data["patronymic"],
                tg_name=data["tg_name"],
                date_of_birth=data["bdate"],
                phone=data["phone"],
                email=data["email"],
                tg_photo=data["tg_photo_path"],
                hobby=data["hobby"],
                surname_eng=data["surname_eng"],
            )
            try:
                await bot.send_photo(operator_list[0], data["photo"],
                                     'Нужно проверить нового пользователя:\n\n'
                                     f'tg_id: {callback_query.from_user.id}\n'
                                     f'{data["surname"]} {data["name"]} {data["patronymic"]}\n'
                                     f'Дата рождения: {data["bdate"]}\n'
                                     f'Телефон: +{data["phone"]}\n'
                                     f'E-mail: {data["email"]}\n'
                                     f'Хобби и увлечения: {data["hobby"]}',
                                     reply_markup=confirm_new_user(data["tg_id"]))
            except CantInitiateConversation:
                await callback_query.message.answer("Оператор не смог ответить, так как не начал чат с ботом.\n"
                                                    "Перешлите пожалуйста эту ошибку отделу кадров")
        await FSM_newbie_questioning.next()
        await bot.edit_message_text("Данные отправлены на обработку модератору",
                                    callback_query.from_user.id,
                                    data["buttons_to_remove"])
        await bot.send_message(callback_query.from_user.id, "Сейчас потребуется 2 минуты концентрации😅"
                                                            "В коротком видео мы расскажем, кто такие ТИМ ФОРСЕРЫ, "
                                                            "а так же кому и по каким вопросам можно обращаться!\n"
                                                            "Начнем? Приятного просмотра😊",
                               reply_markup=keyboard.ok_keyboard())
    else:
        await callback_query.message.edit_text("Укажите что бы вы хотели отредактировать?",
                                               reply_markup=change_newbie_questioning)


# @dp.callback_query_handler(lambda c: c.data.startswith("back"), state="*")
async def back(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    if callback_query.data.split(" ")[1] == "name":
        await FSM_newbie_questioning.asking_surname.set()
        async with state.proxy() as data:
            await data["to_delete"].edit_text("Введи свое ФИО (Например: Пупкин Иван Александрович)")
    elif callback_query.data.split(" ")[1] == "bdate":
        await FSM_newbie_questioning.asking_bday.set()
        async with state.proxy() as data:
            await data["to_delete"].edit_text("Введи свою дату рождения (формат dd.mm.yyyy): ")
    elif callback_query.data.split(" ")[1] == "phone":
        await FSM_newbie_questioning.asking_phone.set()
        async with state.proxy() as data:
            await data["to_delete"].edit_text("Теперь введи свой телефон для связи (формат 7 ХХХ ХХХ ХХХХ): ")
    elif callback_query.data.split(" ")[1] == "email":
        await FSM_newbie_questioning.asking_email.set()
        async with state.proxy() as data:
            await data["to_delete"].edit_text("Укажи свой e-mail (для отправки документов): ")


# @dp.callback_query_handler(lambda c: c.data.startswith("change"), state=FSM_newbie_questioning.commit_data)
async def change_questoning_data(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    if callback_query.data.split(" ")[1] == "name":
        await callback_query.message.edit_text("Введи свое ФИО (Например: Пупкин Иван Александрович):")
        await FSM_newbie_questioning.change_name.set()
    elif callback_query.data.split(" ")[1] == "birth":
        await FSM_newbie_questioning.change_bday.set()
        await callback_query.message.edit_text("Введи свою дату рождения (формат dd.mm.yyyy): ")
    elif callback_query.data.split(" ")[1] == "phone":
        await callback_query.message.edit_text("Теперь введи свой телефон для связи (формат 7 ХХХ ХХХ ХХХХ): ")
        await FSM_newbie_questioning.change_phone.set()
    elif callback_query.data.split(" ")[1] == "e-mail":
        await callback_query.message.edit_text("Укажи свой e-mail (для отправки документов): ")
        await FSM_newbie_questioning.change_email.set()
    elif callback_query.data.split(" ")[1] == "hobbie":
        await callback_query.message.edit_text("Расскажи о своих хобби и увлечениях. "
                                               "Чем любишь заниматься в свободное время? Что тебя вдохновляет "
                                               "и дает энергию?\n"
                                               "Пиши о себе все, чем ты хочешь поделиться с коллегами! "
                                               "Так будет быстрее найти единомышленников и друзей😊")
        await FSM_newbie_questioning.change_hobbie.set()


# @dp.message_handler(state=FSM_newbie_questioning.change_hobbie)
async def change_hobbie(message: types.Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        data["hobby"] = message.text
        data["to_delete"].append(message.message_id)
        data["tg_id"] = message.from_id
        data["tg_name"] = message.from_user.username
    keyboard = Survey_inlines_keyboards()
    await message.answer_photo(data["photo"], 'Проверим, что получилось:\n\n'
                                              f'{data["surname"]} {data["name"]} {data["patronymic"]}\n'
                                              f'Дата рождения: {data["bdate"].strftime("%d.%m.%Y")}\n'
                                              f'Телефон: +{data["phone"]}\n'
                                              f'E-mail: {data["email"]}\n'
                                              f'Хобби и увлечения: {data["hobby"]}')
    await message.answer("Все верно?", reply_markup=keyboard.is_ok())
    await FSM_newbie_questioning.commit_data.set()


# @dp.message_handler(state=FSM_newbie_questioning.change_email)
async def change_email(message: types.Message, state: FSMContext):
    await message.delete()
    validator = validate_email(message.text)
    if validator:
        async with state.proxy() as data:
            data["email"] = message.text
            data["tg_id"] = message.from_id
            data["tg_name"] = message.from_user.username
        keyboard = Survey_inlines_keyboards()
        await message.answer_photo(data["photo"], 'Проверим, что получилось:\n\n'
                                                  f'{data["surname"]} {data["name"]} {data["patronymic"]}\n'
                                                  f'Дата рождения: {data["bdate"].strftime("%d.%m.%Y")}\n'
                                                  f'Телефон: +{data["phone"]}\n'
                                                  f'E-mail: {data["email"]}\n'
                                                  f'Хобби и увлечения: {data["hobby"]}')
        await message.answer("Все верно?", reply_markup=keyboard.is_ok())
        await FSM_newbie_questioning.commit_data.set()
    else:
        async with state.proxy() as data:
            await data["to_delete"].edit_text("Почта введена некорректно.\n"
                                              "Введите корректную почту:")


# @dp.message_handler(state=FSM_newbie_questioning.change_phone)
async def change_phone(message: types.Message, state: FSMContext):
    await message.delete()
    validator = validate_phone(message.text)
    if validator:
        async with state.proxy() as data:
            data["phone"] = validator
            data["tg_id"] = message.from_id
            data["tg_name"] = message.from_user.username
        keyboard = Survey_inlines_keyboards()
        await message.answer_photo(data["photo"], 'Проверим, что получилось:\n\n'
                                                  f'{data["surname"]} {data["name"]} {data["patronymic"]}\n'
                                                  f'Дата рождения: {data["bdate"].strftime("%d.%m.%Y")}\n'
                                                  f'Телефон: +{data["phone"]}\n'
                                                  f'E-mail: {data["email"]}\n'
                                                  f'Хобби и увлечения: {data["hobby"]}')
        await message.answer("Все верно?", reply_markup=keyboard.is_ok())
        await FSM_newbie_questioning.commit_data.set()
    else:
        async with state.proxy() as data:
            await data["to_delete"].edit_text("Необходимо ввести телефон в формате 7 ХХХ ХХХ ХХХХ\n"
                                              "Например 7 917 233 4567")


# @dp.message_handler(state=FSM_newbie_questioning.change_name)
async def change_name(message: types.Message, state: FSMContext):
    await message.delete()
    if is_latin(message.text):
        try:
            name = message.text.split(" ")[1]
            surname = message.text.split(" ")[0]
            patronymic = message.text.split(" ")[2]
            async with state.proxy() as data:
                data["name"] = name
                data["patronymic"] = patronymic
                data["surname"] = surname
                data["tg_id"] = message.from_id
                data["tg_name"] = message.from_user.username
            keyboard = Survey_inlines_keyboards()
            await message.answer_photo(data["photo"], 'Проверим, что получилось:\n\n'
                                                      f'{data["surname"]} {data["name"]} {data["patronymic"]}\n'
                                                      f'Дата рождения: {data["bdate"].strftime("%d.%m.%Y")}\n'
                                                      f'Телефон: +{data["phone"]}\n'
                                                      f'E-mail: {data["email"]}\n'
                                                      f'Хобби и увлечения: {data["hobby"]}')
            await message.answer("Все верно?", reply_markup=keyboard.is_ok())
            await FSM_newbie_questioning.commit_data.set()
        except IndexError:
            async with state.proxy() as data:
                data["to_delete"].edit_text("Необходимо ввести фамилию, имя и отчество, три слова через пробел.\n"
                                            "Введи свое ФИО (Например: Пупкин Иван Александрович):")
    else:
        async with state.proxy() as data:
            await data["to_delete"].edit_text("Пожалуйста, введи свое ФИО на кириллице")


# @dp.message_handler(state=FSM_newbie_questioning.change_bday)
async def change_bday(message: types.Message, state: FSMContext):
    await message.delete()
    validator = validate_bday(message.text)
    if validator:
        async with state.proxy() as data:
            data["bdate"] = validator
            data["tg_id"] = message.from_id
            data["tg_name"] = message.from_user.username
        keyboard = Survey_inlines_keyboards()
        await message.answer_photo(data["photo"], 'Проверим, что получилось:\n\n'
                                                  f'{data["surname"]} {data["name"]} {data["patronymic"]}\n'
                                                  f'Дата рождения: {data["bdate"].strftime("%d.%m.%Y")}\n'
                                                  f'Телефон: +{data["phone"]}\n'
                                                  f'E-mail: {data["email"]}\n'
                                                  f'Хобби и увлечения: {data["hobby"]}')
        await message.answer("Все верно?", reply_markup=keyboard.is_ok())
        await FSM_newbie_questioning.commit_data.set()
    else:
        async with state.proxy() as data:
            await data["to_delete"].edit_text("Необходимо ввести дату в формате dd.mm.yyyy\n"
                                              "(Например 28.07.1989)\n"
                                              "Дата должна быть минимум на 15 лет младше текущей")


# @dp.callback_query_handler(lambda c: c.data == "start", state=FSM_newbie_questioning.show_video)
async def show_video(callback_query: types.CallbackQuery, state: FSMContext):
    keyboard = Survey_inlines_keyboards()
    await state.finish()
    try:
        await bot.send_video(callback_query.from_user.id, message_dict["greeting_video_id"])
    except WrongFileIdentifier as ex:
        print(f"Не удалось загрузить видео:\n"
              f"{ex}")
    await bot.send_message(callback_query.from_user.id,
                           "Теперь у тебя побольше представлений о работе ТИМ ФОРС?\n"
                           "Готов пройти короткий опрос?",
                           reply_markup=keyboard.start_survey())


# ----------------------------------------------------------------------------------------------------------------------

def register_handlers_newbie_questioning(dp: Dispatcher):
    dp.register_callback_query_handler(back, lambda c: c.data.startswith("back"), state="*")
    dp.register_callback_query_handler(questioning_start, lambda c: c.data == "start",
                                       state=FSM_newbie_questioning.newbie_questioning_start)
    dp.register_message_handler(load_surname, state=FSM_newbie_questioning.asking_surname)
    dp.register_callback_query_handler(email_confirming, lambda c: c.data.startswith("answer"),
                                       state=FSM_newbie_questioning.email_creating)
    dp.register_message_handler(load_eng_surname, state=FSM_newbie_questioning.asking_surname_eng)
    dp.register_message_handler(load_bdate, state=FSM_newbie_questioning.asking_bday)
    dp.register_message_handler(load_phone, state=FSM_newbie_questioning.asking_phone)
    dp.register_message_handler(load_email, state=FSM_newbie_questioning.asking_email)
    dp.register_message_handler(load_photo, content_types="photo", state=FSM_newbie_questioning.asking_photo)
    dp.register_message_handler(waiting_for_photo, state=FSM_newbie_questioning.asking_photo)
    dp.register_message_handler(load_hobby, state=FSM_newbie_questioning.asking_hobby)
    dp.register_callback_query_handler(commit_data,
                                       lambda c: c.data.startswith("answer"), state=FSM_newbie_questioning.commit_data)
    dp.register_callback_query_handler(show_video, lambda c: c.data == "start", state=FSM_newbie_questioning.show_video)

    dp.register_callback_query_handler(change_questoning_data,
                                       lambda c: c.data.startswith("change"), state=FSM_newbie_questioning.commit_data)
    dp.register_message_handler(change_name, state=FSM_newbie_questioning.change_name)
    dp.register_message_handler(change_bday, state=FSM_newbie_questioning.change_bday)
    dp.register_message_handler(change_phone, state=FSM_newbie_questioning.change_phone)
    dp.register_message_handler(change_email, state=FSM_newbie_questioning.change_email)
    dp.register_message_handler(change_hobbie, state=FSM_newbie_questioning.change_hobbie)
