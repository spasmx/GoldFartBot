import asyncio
from aiogram import Bot, Dispatcher
from config import settings
from services.reset_state import reset_state_router
from handlers.start import start_router
from handlers.wallets import add_wallet_router, delete_wallet_router, list_wallets_router
from aiogram.fsm.storage.memory import MemoryStorage
from bot.middlewares.db import DbSessionMiddleware
from aiogram.types import BotCommand, BotCommandScopeDefault

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

storage = MemoryStorage()
dp = Dispatcher(storage=storage)
dp.include_router(reset_state_router)
dp.include_router(start_router)
dp.include_router(add_wallet_router)
dp.include_router(delete_wallet_router)
dp.include_router(list_wallets_router)

dp.message.middleware(DbSessionMiddleware())


async def main():
    print("set commands")
    await bot.set_my_commands([
        BotCommand(command="start", description="Запуск бота"),
        BotCommand(command="add", description="Додати гаманець"),
        BotCommand(command="delete", description="Видалити гаманець"),
        BotCommand(command="list", description="Список гаманців")
    ], scope=BotCommandScopeDefault())
    print("Starting bot...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
