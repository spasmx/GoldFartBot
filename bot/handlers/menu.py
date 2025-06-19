from aiogram import Router, types, F, filters
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.state.wallet_states import WalletStates

menu_router = Router()

# Тимчасове зберігання гаманців
wallets = {}


# Головне меню
def main_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text="➕ Додати гаманець", callback_data="menu_add_wallet")
    kb.button(text="📊 Статистика", callback_data="menu_stats")
    kb.button(text="ℹ️ Інформація про мемкойн", callback_data="menu_token_info")
    kb.button(text="⚙️ Налаштування", callback_data="menu_settings")
    kb.adjust(2)
    return kb.as_markup()


def back_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text="⬅️ Назад", callback_data="menu_back")
    kb.adjust(1)
    return kb.as_markup()


@menu_router.message(filters.Command("menu"))
async def show_main_menu(msg: types.Message):
    text = (
        "👋 Вітаю у меню бота!\n\n"
        "Оберіть дію нижче:\n\n"
        "➕ — Додайте гаманець, щоб почати відслідковувати транзакції.\n"
        "📊 — Перегляньте статистику успішних транзакцій.\n"
        "ℹ️ — Дізнайтеся про мемкойн і перегляньте його на Dex Screener.\n"
        "⚙️ — Налаштування бота."
    )
    await msg.answer(text, reply_markup=main_menu())


@menu_router.callback_query()
async def callback_handler(callback: types.CallbackQuery, state: FSMContext):
    data = callback.data

    if data == "menu_add_wallet":
        await callback.message.edit_text(
            "📥 Введіть адресу гаманця:",
            reply_markup=back_menu()
        )
        await state.set_state(WalletStates.waiting_for_wallet_address)

    elif data == "menu_stats":
        user_wallets = wallets.get(callback.from_user.id, [])
        if not user_wallets:
            await callback.message.edit_text("❌ У вас поки немає гаманців.", reply_markup=back_menu())
        else:
            response = "📊 Статистика:\n"
            for w in user_wallets:
                response += f"• {w['name']}: {w['address']}\n"
            await callback.message.edit_text(response, reply_markup=back_menu())
        await callback.answer()

    elif data == "menu_token_info":
        kb = InlineKeyboardBuilder()
        kb.button(text="Переглянути на Dex Screener", url="https://dexscreener.com/solana")
        kb.button(text="⬅️ Назад", callback_data="menu_back")
        kb.adjust(1)
        await callback.message.edit_text("ℹ️ Інформація про мемкойн:", reply_markup=kb.as_markup())
        await callback.answer()

    elif data == "menu_settings":
        await callback.message.edit_text("⚙️ Налаштування (заглушка).", reply_markup=back_menu())
        await callback.answer()

    elif data == "menu_back":
        await callback.message.edit_text("👋 Головне меню:", reply_markup=main_menu())
        await state.clear()
        await callback.answer()


# Стан 1: користувач вводить адресу
@menu_router.message(WalletStates.waiting_for_wallet_address)
async def get_wallet_address(msg: types.Message, state: FSMContext):
    address = msg.text.strip()
    await state.update_data(wallet_address=address)
    await state.set_state(WalletStates.waiting_for_wallet_name)
    await msg.answer("📝 Тепер введіть *назву гаманця*:", parse_mode="Markdown")


# Стан 2: користувач вводить назву
@menu_router.message(WalletStates.waiting_for_wallet_name)
async def get_wallet_name(msg: types.Message, state: FSMContext):
    name = msg.text.strip()
    data = await state.get_data()
    address = data.get("wallet_address")

    user_id = msg.from_user.id
    user_wallets = wallets.get(user_id, [])
    user_wallets.append({"name": name, "address": address})
    wallets[user_id] = user_wallets

    await msg.answer(f"✅ Гаманець '{name}' з адресою `{address}` додано!", parse_mode="Markdown")
    await state.clear()
    await msg.answer("👋 Головне меню:", reply_markup=main_menu())
