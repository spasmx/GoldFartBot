from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.models import Wallet


async def add_wallet(session: AsyncSession, user_id: int, name: str, address: str):
    wallet = Wallet(user_id=user_id, name=name, address=address)
    session.add(wallet)
    await session.commit()
    return wallet


async def get_wallets_by_user(session: AsyncSession, user_id: int):
    result = await session.execute(
        select(Wallet).where(Wallet.user_id == user_id)
    )
    return result.scalars().all()


async def delete_wallet_by_user(session: AsyncSession, user_id: int, name_or_address: str):
    stmt = delete(Wallet).where(
        Wallet.user_id == user_id,
        (Wallet.name == name_or_address) | (Wallet.address == name_or_address)
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0  # True якщо щось видалено