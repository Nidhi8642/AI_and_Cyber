from fastapi import APIRouter
from pydantic import BaseModel
from app.services.ai_assistant_service import build_security_prompt
from app.services.alert_analysis_service import analyze_alert
from app.models.schemas import Alert

router = APIRouter(
    prefix = "/assistant",
    tags= ["AI Security Assistant"]
)

class SecurityAnalysisRequest(BaseModel):
    event_type: str
    severity: str
    message: str

@router.post("/analyze")
def analyze_security_event(request: SecurityAnalysisRequest):
    result = build_security_prompt(
        event_type=request.event_type,
        severity=request.severity,
        message=request.message
    )
    return{
        "event_type" : request.event_type,
        "severity" : request.severity,
        "prompt" : result["prompt"],
        "knowledge" : result["knowledge"]
    }

@router.post("/analyze-alert")
def analyze_alert_endpoint(alert: Alert):
    return analyze_alert(alert)