from fastapi import APIRouter
from app.services.dashboard_service import (get_summary, get_recent_events, get_recent_alerts)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/summary")
def dashboard_summary():
    return get_summary()

@router.get("/events")
def dashboard_events(limit: int = 10):
    return get_recent_events(limit)

@router.get("/alerts")
def dashboard_alerts(limit: int =10):
    return get_recent_alerts(limit)