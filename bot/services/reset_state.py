from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from bot.handlers.start import start_handler
from bot.handlers.wallets.add_wallet import cmd_start_add_wallet
from bot.handlers.wallets.list_wallets import list_wallets
from bot.handlers.wallets.delete_wallet import cmd_start_delete_wallet


reset_state_router = Router()


@reset_state_router.message(Command(commands=["list", "add", "delete", "start"]))
async def reset_state_on_command(msg: Message, state: FSMContext, session: AsyncSession):
    await state.clear()

    if msg.text == "/list":
        await list_wallets(msg, session)
    elif msg.text == "/add":
        await cmd_start_add_wallet(msg, state)
    elif msg.text == "/delete":
        await cmd_start_delete_wallet(msg, state)
    elif msg.text == "/start":
        await start_handler(msg)
