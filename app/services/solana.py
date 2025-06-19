import httpx
import os


async def get_latest_transactions(wallet_address: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            os.getenv("SOLANA_RPC_URL"),
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getSignaturesForAddress",
                "params": [wallet_address]
            }
        )
        return response.json()