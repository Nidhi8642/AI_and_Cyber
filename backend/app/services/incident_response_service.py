from datetime import datetime
from uuid import uuid4
from app.models.schemas import Alert

INCIDENT_STATUSES = [
    "open",
    "investigating",
    "contained",
    "recovering",
    "resolved"
]

def create_incident_from_alert(alert: Alert) -> dict:
    """
    Create a structured incident response workflow from a security alert.
    Incident creation must not depend on external AI services.
    AI analysis can be added separately.
    """

    incident_id = str(uuid4())
    return{
        "incident_id" : incident_id,
        "alert_id" : alert.alert_id,
        "created_at" : datetime.utcnow().isoformat(),
        "status" : "open",
        "identify" : {
            "event_type" : "security alert",
            "severity" : alert.severity.value,
            "reason" : alert.reason,
            "evidence" : alert.evidence,
            "status" : "completed"
        },
        "investigate" : {
            "status":"pending",
            "recommended_steps":[
                "Review the alert evidence.",
                "Review related security alerts.",
                "Identify affected accounts, systems, and services.",
                "Review activity before and after the alert.",
                "Determine whether the activity represents a genuine threat."
            ],
        },
        "correlate" : {
            "status" :"pending",
            "recommended_steps" : [
                "Correlate related authentication events.",
                "Check for successful authentication following failures.",
                "Check for privilege changes or escalation.",
                "Look for additional suspicious activity from the same source."
            ],
        },
        "contain" : {
            "status" : "pending",
            "recommended_steps" : [
                "Restrict suspicious activity when appropriate.",
                "Apply authentication rate limiting where applicable.",
                "Temporarily restrict potentially compromised accounts if evidence supports it.",
                "Increase monitoring of affected systems and accounts."
            ],
            "required_human_approval" : True
        },
        "recover" : {
            "status" : "pending",
            "recommended_steps" : [
                "Reset credentials if compromise is confirmed.",
                "Remove unauthorized access if identified.",
                "Verify affected system integrity.",
                "Continue monitoring after recovery."
            ],
            "requires_human_approval" : True
        },
        "document" : {
            "status" : "pending",
            "recommended_fields" : [
                "Incident timeline",
                "Affected systems",
                "Affected accounts",
                "Evidence collected",
                "Actions taken",
                "Final outcome"
            ],
        },
        "ai_analysis" : None,
        "knowledge" : []
    }

def update_incident_status(incident: dict, new_status: str) -> dict:
    if new_status not in INCIDENT_STATUSES:
        raise ValueError(f"Invalid incident status: {new_status}")
    incident["status"] = new_status
    return incident
