import logging

from settings import config
from aiogram import Bot, Dispatcher, executor
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from db.cache import CacheRedis

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.API_TOKEN, parse_mode="html")
storage = RedisStorage2('localhost', 6379)
dp = Dispatcher(bot, storage=storage)
cache = CacheRedis()

async def on_startup(dp):
    import handlers
    import middlewares
    import filters

    await filters.setup(dp)
    await middlewares.setup(dp)
    # await handlers.dialog.setup(dp)
    await handlers.user.setup(dp)



if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)
