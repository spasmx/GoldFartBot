import asyncio
from aiogram import Bot, Dispatcher
from config import settings
from handlers.menu import menu_router
from handlers.start import start_router
from handlers.wallets import wallets_router

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
dp.include_router(menu_router)
dp.include_router(start_router)
dp.include_router(wallets_router)


async def main():
    print("Starting bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
