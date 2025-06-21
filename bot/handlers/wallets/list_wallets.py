from aiogram import Router, types, filters
from db.crud import get_wallets_by_user
from sqlalchemy.ext.asyncio import AsyncSession

list_wallets_router = Router()


@list_wallets_router.message(filters.Command("list"))
async def list_wallets(msg: types.Message, session: AsyncSession):
    user_id = msg.from_user.id
    wallets = await get_wallets_by_user(session, user_id)

    if not wallets:
        await msg.answer("⚠️ У вас поки немає доданих гаманців.")
        return

    response = "Ваші гаманці:\n"
    for w in wallets:
        response += f"🐳🤑 <b>{w.name}</b> : <code>{w.address}</code>\n"
    await msg.answer(response, parse_mode="HTML")
