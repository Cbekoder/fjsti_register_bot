from aiogram import Dispatcher, Bot, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from asgiref.sync import sync_to_async
import redis.asyncio as redis

from data import config

bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()

router = Router()

dp.include_router(router)


redis_cl = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

@sync_to_async
def orm_async(queryset_or_manager_method, *args, **kwargs):
    return queryset_or_manager_method(*args, **kwargs)