from aiogram import Router, types, filters
from aiogram.fsm.context import FSMContext
from bot.states.wallet_states import WalletStates
from db.crud import add_wallet
from sqlalchemy.ext.asyncio import AsyncSession

add_wallet_router = Router()


@add_wallet_router.message(filters.Command("add"))
async def cmd_start_add_wallet(msg: types.Message, state: FSMContext):
    await msg.answer("📝 Введи назву гаманця:")
    await state.set_state(WalletStates.waiting_for_wallet_name)


@add_wallet_router.message(filters.StateFilter(WalletStates.waiting_for_wallet_name))
async def process_wallet_name(msg: types.Message, state: FSMContext):
    await state.update_data(wallet_name=msg.text.strip())
    await msg.answer("📥 Тепер введи адресу гаманця:")
    await state.set_state(WalletStates.waiting_for_wallet_address)


@add_wallet_router.message(filters.StateFilter(WalletStates.waiting_for_wallet_address))
async def process_wallet_address(
        msg: types.Message,
        state: FSMContext,
        session: AsyncSession
):
    if msg.text.startswith("/"):
        await msg.answer("❌ Адреса не може бути командою. Введи адресу без '/'.")
        return

    data = await state.get_data()
    name = data.get("wallet_name")
    address = msg.text.strip()
    user_id = msg.from_user.id

    wallet = await add_wallet(session, user_id=user_id, name=name, address=address)

    if wallet is None:
        await msg.answer("⚠️ Гаманець з такою назвою або адресою вже існує.")
    else:
        await msg.answer(f"✅ Гаманець <b>{name}</b> з адресою <code>{address}</code> додано!", parse_mode="HTML")

    await state.clear()
