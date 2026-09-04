from fastapi import APIRouter
router = APIRouter(tags=["system"])

@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "outbound-api"}

@router.get("/ready")
def ready() -> dict[str, str]:
    return {"status": "ready"}
