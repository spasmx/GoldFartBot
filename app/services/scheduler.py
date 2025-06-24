from apscheduler.schedulers.asyncio import AsyncIOScheduler
from db.session import async_session_maker
from db.crud import update_wallet_stats
from app.services.solana_tracker import fetch_wallet_stats

scheduler = AsyncIOScheduler()


async def update_all_wallets_stats():
    print("🔁 Запускаємо оновлення статистики всіх гаманців...")

    async with async_session_maker() as session:
        result = await session.execute("SELECT id, user_id, address FROM wallets")
        wallets = result.fetchall()

        for wallet in wallets:
            stats = await fetch_wallet_stats(wallet.address)
            if stats:
                await update_wallet_stats(
                    session=session,
                    wallet_id=wallet.id,
                    win_rate=stats.get("win_rate"),
                    total_trades=stats.get("total_trades"),
                    total_wins=stats.get("total_wins"),
                    total_losses=stats.get("total_losses"),
                    pnl=stats.get("pnl")
                )
    print("✅ Статистика оновлена.")


def start_scheduler():
    scheduler.add_job(update_all_wallets_stats, "interval", hours=48)
    scheduler.start()
