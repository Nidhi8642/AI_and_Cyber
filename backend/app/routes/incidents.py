from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.models.schemas import Alert
from app.services.incident_response_service import (create_incident_from_alert, update_incident_status)

router = APIRouter(
    prefix="/incidents",
    tags=["Incident Response"]
)

class IncidentStatusUpdate(BaseModel):
    status: str

@router.post("/create")
def create_incident(alert:Alert):
    return create_incident_from_alert(alert)

@router.put("/{incident_id}/status")
def update_status(incident_id: str, request: IncidentStatusUpdate):
    #Temporary in-memory incident representation.
    #Persistant incident storage will be added later.
    incident = {"incident_id" : incident_id, "status" : "open"}
    try:
        return update_incident_status(incident, request.status)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))