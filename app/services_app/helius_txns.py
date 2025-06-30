from db.crud import get_user_by_wallets
from app.services_app.token_info import get_token_info
from bot.services.notify import send_token_notification
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.formatting import usd_to_sol, sol_to_usd


async def process_helius_txns(data: list, db: AsyncSession):
    for txn in data:
        if txn.get("type") != "SWAP":
            continue

        wallet_address = txn.get("feePayer")
        if not wallet_address:
            continue

        token_transfers = txn.get("tokenTransfers", [])
        if len(token_transfers) == 0:
            continue

        if len(token_transfers) >= 2:
            token_out = token_transfers[0]
            token_in = token_transfers[1]

            swap_type = "buy"
            token_address = token_out["mint"]
            native_amount = token_in["tokenAmount"]

        elif len(token_transfers) == 1:
            token_out = token_transfers[0]
            swap_type = "sell"
            token_address = token_out["mint"]
            native_amount = token_out["tokenAmount"]

        else:
            continue

        token_event = {
            "tokenAddress": token_address,
            "nativeAmount": native_amount,
            "usdAmount": None,
            "dex": txn.get("source")
        }

        token_info = await get_token_info(token_event)
        if swap_type == "buy":
            token_event["usdAmount"] = sol_to_usd(token_event.get("nativeAmount"))
        else:
            token_event["nativeAmount"] = usd_to_sol(token_event.get("nativeAmount"),
                                                     float(token_info.get("token_price_usd")))
            token_event["usdAmount"] = sol_to_usd(token_event.get("nativeAmount"))

        user_ids = await get_user_by_wallets(db, wallet_address)

        for user in user_ids:
            await send_token_notification(
                user.user_id,
                user.name,
                wallet_address,
                swap_type,
                token_info,
                token_event
            )
