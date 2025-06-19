from aiogram import Router, types, filters, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

wallets_router = Router()


class AddWallet(StatesGroup):
    waiting_for_name = State()
    waiting_for_address = State()


wallets = {}


@wallets_router.message(filters.Command("add"))
async def wallet_name(msg: types.Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer("Введи адресу гаманця:")
    await state.set_state(AddWallet.waiting_for_address)


@wallets_router.message(F.state == AddWallet.waiting_for_name)
async def cmd_add_wallet(msg: types.Message, state: FSMContext):
    await msg.answer("Введи назву гаманця:")
    await state.set_state(AddWallet.waiting_for_name)


@wallets_router.message(F.state == AddWallet.waiting_for_address)
async def wallet_address(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data.get("name")
    address = msg.text

    user_wallets = wallets.get(msg.from_user.id, [])
    user_wallets.append({"name": name, "address": address})
    wallets[msg.from_user.id] = user_wallets

    await msg.answer(f"Гаманець '{name}' з адресою {address} додано.")
    await state.clear()


@wallets_router.message(filters.Command("list"))
async def list_wallets(msg: types.Message):
    user_wallets = wallets.get(msg.from_user.id, [])
    if not user_wallets:
        await msg.answer("У вас поки немає доданих гаманців.")
        return

    response = "Ваші гаманці:\n"
    for w in user_wallets:
        response += f"• {w['name']}: {w['address']}\n"
    await msg.answer(response)


@wallets_router.message(filters.Command("stats"))
async def stats_all_wallets(msg: types.Message):
    user_wallets = wallets.get(msg.from_user.id, [])

    if not user_wallets:
        await msg.answer("У тебе поки немає доданих гаманців.")
        return

    # Заглушка: фейкові дані для кожного гаманця
    response_lines = []
    total_transactions_all = 0
    successful_transactions_all = 0

    for wallet in user_wallets:
        total = 100  # фейкові загальні транзакції
        successful = 75  # фейкові успішні транзакції
        winrate = (successful / total) * 100

        total_transactions_all += total
        successful_transactions_all += successful

        response_lines.append(
            f"Гаманець '{wallet['name']}':\n"
            f"  Всього транзакцій: {total}\n"
            f"  Успішних транзакцій: {successful}\n"
            f"  Winrate: {winrate:.2f}%\n"
        )

    # Загальна статистика по всіх гаманцях
    overall_winrate = (successful_transactions_all / total_transactions_all) * 100 if total_transactions_all > 0 else 0

    response_lines.append(
        f"\nЗагальна статистика по всіх гаманцях:\n"
        f"  Всього транзакцій: {total_transactions_all}\n"
        f"  Успішних транзакцій: {successful_transactions_all}\n"
        f"  Загальний Winrate: {overall_winrate:.2f}%"
    )

    await msg.answer("\n".join(response_lines))
