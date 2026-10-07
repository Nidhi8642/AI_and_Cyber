from app.models.schemas import SecurityEvent

EVENT_TYPE_MAPPING = {
    "authentication_failure": 1,
    "authentication_success": 2,
    "user_login": 3,
    "privilege_escalation": 4,
    "unknown": 0
}

SEVERITY_MAPPING ={
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}

def extract_features(event: SecurityEvent) -> list[float]:
    """
    Convert a SecurityEvent into numerical features that can be used by an ML anomaly detection model.
    """

    event_type = EVENT_TYPE_MAPPING.get(event.event_type, 0)
    severity = SEVERITY_MAPPING.get(event.severity.value, 1)

    has_source_ip = 1 if event.source_ip else 0
    has_username = 1 if event.username else 0
    has_service = 1 if event.service else 0

    return [
        float(event_type),
        float(severity),
        float(has_source_ip),
        float(has_username),
        float(has_service)
    ]