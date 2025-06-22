from fastapi import APIRouter

router = APIRouter()

@router.get("/math/add")
async def add(x: float, y: float):
    """Return the sum of two numbers."""
    return {"result": x + y}
