from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_async_session
from db.crud import get_all_wallet_addresses
from app.services_app.helius_webhook import (
    create_helius_webhook,
    delete_helius_webhook,
    list_helius_webhooks,
    update_helius_webhook,
)
from config import settings
from pydantic import BaseModel
from typing import List

router = APIRouter()


class UpdateWebhookRequest(BaseModel):
    webhookURL: str
    accountAddresses: List[str]
    transactionTypes: List[str] = ["SWAP"]
    webhookType: str = "enhanced"
    encoding: str = "json"


@router.post("/create")
async def create_webhook(db: AsyncSession = Depends(get_async_session)):
    addresses = await get_all_wallet_addresses(db)
    webhook_url = settings.HELIUS_WEBHOOK_URL
    response = await create_helius_webhook(webhook_url, addresses)
    return response


@router.get("/list")
async def list_webhooks():
    response = await list_helius_webhooks()
    return response


@router.delete("/delete/{webhook_id}")
async def delete_webhook(webhook_id: str):
    success = await delete_helius_webhook(webhook_id)
    if not success:
        raise HTTPException(status_code=404, detail="Webhook not found or could not be deleted.")
    return {"detail": f"Webhook {webhook_id} deleted successfully."}


@router.put("/update/{webhook_id}")
async def update_webhook(db: AsyncSession = Depends(get_async_session)):
    addresses = await get_all_wallet_addresses(db)
    webhook_url = settings.HELIUS_WEBHOOK_URL
    response = await update_helius_webhook(webhook_url, addresses)
    return response

