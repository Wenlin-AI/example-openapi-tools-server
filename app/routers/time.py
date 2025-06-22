from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/time")
async def current_time():
    """Return the current UTC time."""
    return {"time": datetime.utcnow().isoformat() + "Z"}
