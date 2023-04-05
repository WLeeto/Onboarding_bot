import asyncio

from aiogram.utils import executor
from create_bot import dp
from func.all_func import set_default_commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from middleware.scheldule_middleware import SchedulerMiddleware


async def on_startup(_):
    """
    Запуск бота
    """
    asyncio.create_task(set_default_commands(dp))

    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.start()

    dp.middleware.setup(SchedulerMiddleware(scheduler))

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


