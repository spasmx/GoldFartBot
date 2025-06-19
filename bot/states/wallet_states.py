from aiogram.fsm.state import StatesGroup, State


class WalletStates(StatesGroup):
    waiting_for_wallet_address = State()
    waiting_for_wallet_name = State()
