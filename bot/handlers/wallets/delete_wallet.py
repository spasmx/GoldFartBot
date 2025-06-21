from aiogram import Router, types, filters
from aiogram.fsm.context import FSMContext
from bot.states.wallet_states import WalletStates
from db.crud import delete_wallet_by_user
from sqlalchemy.ext.asyncio import AsyncSession

delete_wallet_router = Router()


@delete_wallet_router.message(filters.Command("delete"))
async def cmd_start_delete_wallet(msg: types.Message, state: FSMContext):
    await msg.answer("❌ Вкажи назву або адресу гаманця: `MyWallet` або `Hf1Z...`",
                     parse_mode="Markdown")
    await state.set_state(WalletStates.waiting_for_wallet_delete)


@delete_wallet_router.message(filters.StateFilter(WalletStates.waiting_for_wallet_delete))
async def process_delete_wallet(msg: types.Message, state: FSMContext, session: AsyncSession):
    name_or_address = msg.text.strip()
    user_id = msg.from_user.id

    success = await delete_wallet_by_user(session, user_id=user_id, name_or_address=name_or_address)

    if success:
        await msg.answer("✅ Гаманець успішно видалено.")
    else:
        await msg.answer("⚠️ Гаманець не знайдено.")
    await state.clear()
