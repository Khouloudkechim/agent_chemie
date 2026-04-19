from fastapi import APIRouter

router = APIRouter()

# Placeholder for history. In a real app, this would query a database.
@router.get("/history")
async def get_history():
    return []
