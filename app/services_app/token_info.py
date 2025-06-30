import httpx
from app.utils.formatting import format_number


async def get_token_info(event: dict) -> dict:
    token_address = event.get("tokenAddress")
    if not token_address:
        return {}

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            resp = await client.get(f"https://api.dexscreener.com/tokens/v1/solana/{token_address}")
            resp.raise_for_status()
            data = resp.json()
            # очікується список пар
            pair_data = data[0] if isinstance(data, list) and len(data) > 0 else None
        except (httpx.HTTPError, ValueError, IndexError):
            pair_data = None

    if not pair_data:
        return {
            "token_name": "Unknown Token",
            "token_address": token_address,
            "token_price": "",
            "token_price_usd": "",
            "market_cap": "N/A",
            "liquidity": "N/A",
            "is_burned": False,
            "ath": "N/A",
            "dexscreener": f"https://dexscreener.com/solana/{token_address}",
            "gngm": f"https://gngm.xyz/token/{token_address}",
            "axiom": f"https://axiom.xyz/token/{token_address}",
        }

    base_token = pair_data.get("baseToken", {})
    token_name = base_token.get("name", "Unknown Token")
    dex_url = pair_data.get("url", f"https://dexscreener.com/solana/{token_address}")
    token_price = pair_data.get("priceNative")
    token_price_usd = pair_data.get("priceUsd")

    market_cap = pair_data.get("marketCap")
    liquidity = pair_data.get("liquidity", {}).get("usd")

    return {
        "token_name": token_name,
        "token_address": token_address,
        "token_price": token_price,
        "token_price_usd": token_price_usd,
        "market_cap": format_number(market_cap) if market_cap else "N/A",
        "liquidity": format_number(liquidity) if liquidity else "N/A",
        "dexscreener": dex_url,
        "gngm": f"https://gngm.xyz/token/{token_address}",
        "axiom": f"https://axiom.xyz/token/{token_address}",
    }
