import httpx
from config import settings

HEADERS = {
    "Content-Type": "application/json",
}

BASE_PARAMS = {"api-key": settings.HELIUS_API_KEY}


async def create_helius_webhook(webhook_url: str, address_list: list[str]) -> dict:
    payload = {
        "webhookURL": webhook_url,
        "transactionTypes": ["SWAP"],
        "accountAddresses": address_list,
        "webhookType": "enhanced",
        "encoding": "json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                settings.HELIUS_BASE_URL,
                params=BASE_PARAMS,
                headers=HEADERS,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise RuntimeError(f"❌ Helius error: {e.response.status_code} — {e.response.text}")


async def update_helius_webhook(webhook_url: str, address_list: dict) -> dict:
    webhook_id = settings.WEBHOOK_ID
    payload = {
        "webhookURL": webhook_url,
        "transactionTypes": ["SWAP"],
        "accountAddresses": address_list,
        "webhookType": "enhanced",
        "encoding": "json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(
                f"{settings.HELIUS_BASE_URL}{webhook_id}",
                params=BASE_PARAMS,
                headers=HEADERS,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise RuntimeError(f"❌ Update Helius error: {e.response.status_code} — {e.response.text}")


async def delete_helius_webhook(webhook_id: str) -> bool:
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"{settings.HELIUS_BASE_URL}{webhook_id}",
            params=BASE_PARAMS
        )
        return response.status_code == 200


async def list_helius_webhooks() -> list[dict]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            settings.HELIUS_BASE_URL,
            params=BASE_PARAMS
        )
        response.raise_for_status()
        return response.json()
