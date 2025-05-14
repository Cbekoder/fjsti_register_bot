import os
import sys
import django
from asyncio import run
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DJANGO_PROJECT_PATH = os.path.join(BASE_DIR, "admin")

sys.path.append(DJANGO_PROJECT_PATH)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from loader import bot, dp
import handlers



async def on_startup():
    await on_startup_notify()
    await set_default_commands()

async def main() -> None:
    dp.startup.register(on_startup)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    run(main())
