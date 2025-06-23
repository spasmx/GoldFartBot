import aiohttp
from config import settings


async def fetch_wallet_stats(address: str) -> dict:
    url = f"{settings.SOLANA_TRACKER_URL}{address}"
    headers = {"x-api-key": settings.SOLANA_TRACKER_TOKEN}
    params = {"hideDetails": "true"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as resp:
            print("------------------------------------")
            print(resp.url)
            print(resp.headers)
            print(resp.status)
            print("------------------------------------")
            if resp.status == 200:
                data = await resp.json()
                summary = data.get("summary")
                print(type(summary.get("total")))
                return {
                    "win_rate": summary.get("winPercentage", 0.0),
                    "total_trades": summary.get("totalWins", 0) + summary.get("totalLosses", 0),
                    "pnl": round(summary.get("total"), 2),
                }
            else:
                return None