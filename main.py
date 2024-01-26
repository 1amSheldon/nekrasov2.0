import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import betterlogging as bl
from config.config_reader import config
from handlers import start, gpt,admin, roles, support, model


logger = logging.getLogger(__name__)
log_level = logging.INFO
bl.basic_colorized_config(level=log_level)
VERSION = 1.1

# u can find me on tg: @iamsheldon


async def main():
    logging.basicConfig(
        format="%(filename)s [LINE:%(lineno)d] #%(levelname)-6s [%(asctime)s]  %(message)s",
        datefmt="%d.%m.%Y %H:%M:%S",
        level=log_level,
    )

    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="MarkdownV2")

    dp.include_routers(model.router, roles.router, gpt.router,admin.router, support.router, start.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
