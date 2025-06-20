from aiogram import Router, types, filters, F
from aiogram.filters import CommandObject
from aiogram.fsm.context import FSMContext
from bot.states.wallet_states import WalletStates
from db.crud import add_wallet, get_wallets_by_user, delete_wallet_by_user
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_async_session


wallets_router = Router()


@wallets_router.message(filters.Command("add"))
async def cmd_start_add_wallet(msg: types.Message, state: FSMContext):
    await msg.answer("📝 Введи назву гаманця:")
    await state.set_state(WalletStates.waiting_for_wallet_name)
    print(state)


@wallets_router.message(filters.StateFilter(WalletStates.waiting_for_wallet_name))
async def process_wallet_name(msg: types.Message, state: FSMContext):
    await state.update_data(wallet_name=msg.text.strip())
    await msg.answer("📥 Тепер введи адресу гаманця:")
    await state.set_state(WalletStates.waiting_for_wallet_address)


@wallets_router.message(filters.StateFilter(WalletStates.waiting_for_wallet_address))
async def process_wallet_address(
        msg: types.Message,
        state: FSMContext,
        session: AsyncSession
):
    data = await state.get_data()
    name = data.get("wallet_name")
    address = msg.text.strip()
    user_id = msg.from_user.id

    await add_wallet(session, user_id=user_id, name=name, address=address)
    await msg.answer(f"✅ Гаманець '{name}' з адресою `{address}` додано!", parse_mode="Markdown")
    await state.clear()


# @wallets_router.message(filters.Command("list"))
# async def list_wallets(msg: types.Message, session: AsyncSession):
#     user_id = msg.from_user.id
#     wallets = await get_wallets_by_user(session, user_id)
#
#     if not wallets:
#         await msg.answer("У вас поки немає доданих гаманців.")
#         return
#
#     response = "Ваші гаманці:\n"
#     for w in wallets:
#         response += f"• {w.name}: {w.address}\n"
#     await msg.answer(response)


@wallets_router.message(filters.Command("delete"))
async def delete_wallet(msg: types.Message, command: CommandObject, session: AsyncSession):
    args = command.args
    if not args:
        await msg.answer("❌ Вкажи назву або адресу гаманця: `/delete MyWallet` або `/delete Hf1Z...`",
                         parse_mode="Markdown")
        return

    user_id = msg.from_user.id

    success = await delete_wallet_by_user(session, user_id=user_id, name_or_address=args.strip())

    if success:
        await msg.answer("✅ Гаманець успішно видалено.")
    else:
        await msg.answer("⚠️ Гаманець не знайдено.")
#
#
# @wallets_router.message(filters.Command("stats"))
# async def stats_all_wallets(msg: types.Message, session: AsyncSession = F.depends(get_async_session)):
#     user_id = msg.from_user.id
#     wallets = await get_wallets_by_user(session, user_id)
#
#     if not wallets:
#         await msg.answer("У тебе поки немає доданих гаманців.")
#         return
#
#     # Заглушка для статистики
#     response_lines = []
#     total_transactions_all = 0
#     successful_transactions_all = 0
#
#     for wallet in wallets:
#         total = 100  # фейкові загальні транзакції
#         successful = 75  # фейкові успішні транзакції
#         winrate = (successful / total) * 100
#
#         total_transactions_all += total
#         successful_transactions_all += successful
#
#         response_lines.append(
#             f"Гаманець '{wallet.name}':\n"
#             f"  Всього транзакцій: {total}\n"
#             f"  Успішних транзакцій: {successful}\n"
#             f"  Winrate: {winrate:.2f}%\n"
#         )
#
#     overall_winrate = (successful_transactions_all / total_transactions_all) * 100 if total_transactions_all > 0 else 0
#
#     response_lines.append(
#         f"\nЗагальна статистика по всіх гаманцях:\n"
#         f"  Всього транзакцій: {total_transactions_all}\n"
#         f"  Успішних транзакцій: {successful_transactions_all}\n"
#         f"  Загальний Winrate: {overall_winrate:.2f}%"
#     )
#
#     await msg.answer("\n".join(response_lines))
