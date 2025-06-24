from sqlalchemy import delete, and_, or_, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.models import Wallet
from datetime import datetime


async def add_wallet(session: AsyncSession, user_id: int, name: str, address: str,
                     win_rate: float = None, total_trades: int = None, total_wins: int = None,
                     total_losses: int = None, pnl: float = None):
    # Перевірка на дублікати по назві або адресі
    result = await session.execute(
        select(Wallet).where(
            Wallet.user_id == user_id,
            (Wallet.name == name) | (Wallet.address == address)
        )
    )
    existing = result.scalars().first()
    if existing:
        return None  # сигнал, що гаманець уже існує

    wallet = Wallet(user_id=user_id, name=name, address=address, win_rate=win_rate, total_trades=total_trades,
                    total_wins=total_wins, total_losses=total_losses,pnl=pnl)
    session.add(wallet)
    await session.commit()
    return wallet


async def update_wallet_stats(session: AsyncSession, wallet_id: int, win_rate: float, total_trades: int,
                              total_wins: int, total_losses: int, pnl: float):
    stmt = (
        update(Wallet)
        .where(Wallet.id == wallet_id)
        .values(
            win_rate=win_rate,
            total_trades=total_trades,
            total_wins=total_wins,
            total_losses=total_losses,
            pnl=pnl,
            updated_at=datetime.utcnow()
        )
    )
    await session.execute(stmt)
    await session.commit()


async def get_wallets_by_user(session: AsyncSession, user_id: int):
    result = await session.execute(
        select(Wallet).where(Wallet.user_id == user_id)
    )
    return result.scalars().all()


async def delete_wallet_by_user(session: AsyncSession, user_id: int, name_or_address: str):
    stmt = delete(Wallet).where(
        and_(
            Wallet.user_id == user_id,
            or_(
                Wallet.name == name_or_address,
                Wallet.address == name_or_address
            )
        )
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0
