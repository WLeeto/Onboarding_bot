from aiogram import Bot
# from aiogram.contrib.fsm_storage.redis import RedisStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from os import environ

from database.requests import database

from aiogram import types

storage = MemoryStorage()
# storage = RedisStorage('redis://localhost:6379/0')

token_tg = environ.get("TOKEN_ONBOARDING_BOT")

bot = Bot(token=token_tg)

dp = Dispatcher(bot, storage=storage)

db = database()

