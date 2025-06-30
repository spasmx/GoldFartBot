from aiogram import Router, types, filters
from db.crud import get_wallets_by_user
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.context import FSMContext
from bot.services.pagination import send_paginated_page

list_wallets_router = Router()

PAGE_SIZE = 5


def render_wallet_simple(wallet):
    return f"🐳🤑 <a href='https://www.solanatracker.io/wallet/{wallet.address}'>{wallet.name}</a>" \
           f" : <code>{wallet.address}</code>\n"


@list_wallets_router.message(filters.Command("list"))
async def list_wallets(msg: types.Message, session: AsyncSession, state: FSMContext):
    user_id = msg.from_user.id
    wallets = await get_wallets_by_user(session, user_id)

    if not wallets:
        await msg.answer("⚠️ У вас поки немає доданих гаманців.")
        return

    await state.update_data(wallets=wallets)
    await send_paginated_page(
        msg,
        wallets,
        page=0,
        page_size=PAGE_SIZE,
        render_item_fn=render_wallet_simple,
        callback_prefix="list_page",
        title="Ваші гаманці"
    )


@list_wallets_router.callback_query(lambda c: c.data and c.data.startswith("list_page_"))
async def list_page_callback(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    wallets = data.get("wallets", [])
    page = int(callback.data.split("_")[-1])

    await state.update_data(page=page)
    await send_paginated_page(
        callback,
        wallets,
        page=page,
        page_size=PAGE_SIZE,
        render_item_fn=render_wallet_simple,
        callback_prefix="list_page",
        title="Ваші гаманці"
    )
    await callback.answer()
