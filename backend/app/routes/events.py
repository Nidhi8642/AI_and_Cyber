from fastapi import APIRouter, FastAPI
from app.models.schemas import SecurityEvent

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)

@router.post("/")
def create_event(event: SecurityEvent):
    return {
        "message": " Security event received",
        "event": event
    }