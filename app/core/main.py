from fastapi import FastAPI
from app.api.router import router as helius_router
from app.api.webhook_admin import router as admin_router

app = FastAPI()

app.include_router(helius_router, prefix="/helius/webhook", tags=["helius"])

app.include_router(admin_router, prefix="/helius/webhook/admin", tags=["admin"])

