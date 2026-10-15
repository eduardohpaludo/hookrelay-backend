from fastapi import APIRouter

webhook_router = APIRouter(prefix="/webhooks", tags=["webhooks"])

@webhook_router.get("/")
async def list_webhooks():
    """
    Default webhooks route
    """
    return {"status": "ok"}