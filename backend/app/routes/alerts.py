from fastapi import APIRouter
from app.models.schemas import Alert

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)

@router.post("/")
def create_alert(alert: Alert):
    return {
        "message": "Alert received",
        "alert": alert
    }