import html
from bot.bot_instance import bot


async def send_token_notification(user_id, wallet_name, wallet_address: str, swap_type: str, info: dict,
                                  token_event: dict):
    emoji = "🟢" if swap_type == "buy" else "🔴"

    wallet_address_safe = html.escape(wallet_address)

    token_name = html.escape(info.get("token_name", "Unknown Token"))
    token_price = info.get("token_price")
    token_price_usd = info.get("token_price_usd")
    market_cap = info.get("market_cap", "N/A")
    liquidity = info.get("liquidity", "N/A")
    dex = token_event.get("dex")
    amount_sol = round(float(token_event.get("nativeAmount")), 2)
    amount_usd = round(float(token_event.get("usdAmount")), 2)

    # fallback links
    dexscreener = info.get("dexscreener") or "#"
    gngm = info.get("gngm") or "#"
    axiom = info.get("axiom") or "#"

    message = (
        f"{emoji} <b>{swap_type.upper()} {token_name} on {dex}</b>\n"
        f"👤<b>{wallet_name}</b>\n"
        f"<code>{wallet_address_safe}</code>\n"
        f"💰 <b>{amount_sol} SOL</b> (${amount_usd})\n\n"
        f"🪙 <b>{token_name}</b>\n"
        f"🔗 "
        f"<a href='{dexscreener}'>DexScreener</a> | "
        f"<a href='{gngm}'>GNGM</a> | "
        f"<a href='{axiom}'>Axiom</a>\n\n"
        f"🏋️ <b>{token_price} SOL</b> (${token_price_usd})\n\n"
        f"📊 Market Cap: <b>{market_cap}</b>\n"
        f"💦 liq: <b>{liquidity}</b>"
    )

    try:
        await bot.send_message(chat_id=user_id, text=message, parse_mode="HTML", disable_web_page_preview=True)
    except Exception as e:
        print("❌ Error sending message:", e)
        print("🔍 Message content:", message)



