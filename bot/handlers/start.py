from aiogram import types, Router, filters
start_router = Router()


@start_router.message(filters.Command("start"))
async def start_handler(msg: types.Message):
    text = (
        "👋 Привіт лудік!\n\n"
        "Cписок доступних команд:\n\n"
        "🔘 /start — Перезапустити бота\n"
        # "🔘 /menu — Відкрити головне меню\n"
        "🔘 /add — Додати гаманець\n"
        "🔘 /delete — Видалити гаманець\n"
        # "🔘 /list — Показати всі ваші гаманці\n"
        # "🔘 /stats — Переглянути статистику\n"
    )
    await msg.answer(text)
