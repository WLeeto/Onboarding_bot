from aiogram import types
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from create_bot import dp, bot, db


async def _send_message(chat_id, text):
    await bot.send_message(chat_id=chat_id, text=text)
    print(f"Произведена отсроченная отправка для {chat_id}")


async def send_schelduled_message(scheduler: AsyncIOScheduler, **kwargs):
    """
    Планирует отправку сообщения на определенную дату/время
    :param scheduler: None
    :param kwargs: run_date=obj(datetime), text=str, chat_id=int
    :return: None
    """
    scheduler.add_job(_send_message, trigger="date",
                      run_date=kwargs["run_date"],
                      args=(kwargs["chat_id"], kwargs["text"] + " " + kwargs["run_date"].str))
    print(f"Добавлена новая отсроченная отправка на {kwargs['run_date']} для {kwargs['chat_id']}")
