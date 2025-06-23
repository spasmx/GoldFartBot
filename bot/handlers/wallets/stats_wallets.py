from aiogram import Router, types, filters
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from db.crud import get_wallets_by_user
from bot.services.pagination import send_paginated_page

stats_wallets_router = Router()

# stats_wallets.py



PAGE_SIZE = 5


def render_wallet_stats(wallet):
    return (
        f"👜 <b>{wallet.name}</b>\n"
        f"🔗 <code>{wallet.address}</code>\n"
        f"🎯 Winrate: <b>{wallet.win_rate:.2f}%</b>\n"
        f"📈 Total Trades: {wallet.total_trades}\n"
        f"✅ PnL: {wallet.pnl}\n\n"
    )


def add_tracker_links(builder, wallets):
    for w in wallets:
        builder.button(
            text=f"🌐 Відкрити {w.name} в Solana Tracker",
            url=f"https://www.solanatracker.io/wallet/{w.address}"
        )


@stats_wallets_router.message(filters.Command("stats"))
async def stats_all_wallets(msg: types.Message, session: AsyncSession, state: FSMContext):
    user_id = msg.from_user.id
    wallets = await get_wallets_by_user(session, user_id=user_id)

    if not wallets:
        await msg.answer("⚠️ У вас немає збережених гаманців.")
        return

    sorted_wallets = sorted(wallets, key=lambda w: w.win_rate or 0, reverse=True)

    await state.update_data(wallets=sorted_wallets)
    await send_paginated_page(
        msg,
        sorted_wallets,
        page=0,
        page_size=PAGE_SIZE,
        render_item_fn=render_wallet_stats,
        callback_prefix="stats_page",
        title="Статистика гаманців",
        extra_buttons_fn=add_tracker_links
    )


@stats_wallets_router.callback_query(lambda c: c.data and c.data.startswith("stats_page_"))
async def stats_page_callback(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    wallets = data.get("wallets", [])
    page = int(callback.data.split("_")[-1])

    await state.update_data(page=page)
    await send_paginated_page(
        callback,
        wallets,
        page=page,
        page_size=PAGE_SIZE,
        render_item_fn=render_wallet_stats,
        callback_prefix="stats_page",
        title="Статистика гаманців",
        extra_buttons_fn=add_tracker_links
    )
    await callback.answer()
