import asyncio
import datetime
import re

from aiogram import Bot
from aiogram.utils import executor
from apscheduler.jobstores.redis import RedisJobStore

from create_bot import dp, bot, db
from func.all_func import set_default_commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from func.scheldule import _send_message
from middleware.scheldule_middleware import SchedulerMiddleware

from apscheduler_di import ContextSchedulerDecorator
from apscheduler.jobstores.redis import RedisJobStore


async def on_startup(_):
    """
    Запуск бота
    """
    asyncio.create_task(set_default_commands(dp))

    # job_stores = {
    #     "default": RedisJobStore(
    #         jobs_key="dispatched_trips_jobs", run_times_key="dispatched_trips_running",
    #         host="redis", port=6379
    #     )
    # }

    # scheduler = ContextSchedulerDecorator(AsyncIOScheduler(jobstores=job_stores, timezone="Europe/Moscow"))
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    # scheduler.ctx.add_instance(bot, declared_class=Bot)
    scheduler.start()
    dp.middleware.setup(SchedulerMiddleware(scheduler))
    db.create_tables()

    all_scheldulered_message = db.get_all_scheldulered_message()
    for i in all_scheldulered_message:
        if i.date_to_send >= datetime.datetime.utcnow() + datetime.timedelta(hours=3, minutes=6):
            recipient = db.find_user_by_id(i.to_id)
            scheduler.add_job(_send_message, trigger="date", run_date=i.date_to_send - datetime.timedelta(minutes=5),
                      kwargs={"chat_id": recipient.tg_id,
                              "text": i.text},
                      timezone='Europe/Moscow')
            print(f"Добавлена отложенная отправка: {i.date_to_send} {recipient.tg_name}")
        else:
            db.delete_scheldulered_message(i.id)
    db.session.close()

    print('Бот запущен')


async def on_shutdown(_):
    """
    Завершение работы
    """
    print('Бот отключен')


from handlers import client, admin, other

admin.register_handlers_admin(dp)
client.register_handlers_client(dp)
other.register_handlers_other(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)


