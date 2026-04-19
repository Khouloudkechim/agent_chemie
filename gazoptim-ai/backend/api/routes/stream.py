from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse
import asyncio

router = APIRouter()

# Note: In a real app, you would use Redis pub/sub or an Event Bus to 
# stream LangGraph node executions. Here we provide a mock stream for the frontend demo.
@router.get("/stream/{session_id}")
async def stream_progress(session_id: str):
    async def event_generator():
        steps = [
            "Analyse de la composition gazeuse...",
            "Vérification des paramètres de sécurité...",
            "Évaluation du potentiel énergétique...",
            "Prise de décision par l'IA...",
            "Génération du rapport..."
        ]
        
        for step in steps:
            await asyncio.sleep(1.5)
            yield {
                "event": "message",
                "id": "message_id",
                "retry": 15000,
                "data": step
            }
        
        yield {
            "event": "message",
            "data": "DONE"
        }

    return EventSourceResponse(event_generator())
