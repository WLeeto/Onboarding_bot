from aiogram import types
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from create_bot import dp, bot, db


async def _send_message(chat_id, text):
    await bot.send_message(chat_id=chat_id, text=text, parse_mode=types.ParseMode.HTML)
    print(f"Произведена отсроченная отправка для {chat_id}")


async def _send_message_with_photo(chat_id, text, photo_id):
    await bot.send_photo(chat_id=chat_id, photo=photo_id, caption=text, parse_mode=types.ParseMode.HTML)
    print(f"Произведена отсроченная отправка для {chat_id}")


async def _send_exeption(chat_id, text):
    await bot.send_message(chat_id=chat_id, text=text)
    print(f"Не получилось запланировать отправку\n{text}")

