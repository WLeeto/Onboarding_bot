from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from os import environ

from database.requests import database

storage = MemoryStorage()

token_tg = environ.get("TOKEN_ONBOARDING_BOT")

bot = Bot(token=token_tg)
dp = Dispatcher(bot, storage=storage)

db = database()
db.create_tables()
