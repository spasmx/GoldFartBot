import requests


def format_number(num: float | str | None) -> str:
    try:
        num = float(num)
    except (TypeError, ValueError):
        return "N/A"

    if num >= 1_000_000_000:
        return f"{num / 1_000_000_000:.1f}B"
    elif num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    else:
        return str(int(num))


def get_sol_usd_rate():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return data['solana']['usd']


def sol_to_usd(amount_sol):
    rate = get_sol_usd_rate()
    return round(float(amount_sol * rate), 2)


def usd_to_sol(token_amount: float, token_price_usd: float) -> float:
    total_usd = token_amount * token_price_usd
    sol_rate = get_sol_usd_rate()
    return round(float(total_usd / sol_rate), 6)
