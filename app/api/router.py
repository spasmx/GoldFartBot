from fastapi import APIRouter, Request, Depends, HTTPException
from app.services_app.helius_txns import process_helius_txns
from db.session import get_async_session as get_db
from sqlalchemy.ext.asyncio import AsyncSession
import logging
import json

router = APIRouter()


@router.post("/")
async def helius_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        data = await request.json()
        print("🔔 Webhook received from Helius:", json.dumps(data, indent=2))
        with open("helius_resp.json", "a", encoding="utf-8") as f:
            f.write(json.dumps(data, indent=2) + "\n\n")
        logging.info("✅ Received webhook from Helius")
        await process_helius_txns(data, db)
        return {"status": "ok"}
    except Exception as e:
        logging.error(f"❌ Failed to process Helius webhook: {e}")
        raise HTTPException(status_code=400, detail="Failed to process webhook")
