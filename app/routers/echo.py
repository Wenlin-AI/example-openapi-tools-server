from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class EchoRequest(BaseModel):
    message: str

@router.post("/echo")
async def echo_message(payload: EchoRequest):
    """Echo back the provided message."""
    return {"message": payload.message}
