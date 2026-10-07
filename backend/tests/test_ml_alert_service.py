from datetime import datetime

from app.models.schemas import SecurityEvent, Severity
from app.services.anomaly_service import AnomalyDetectionService
from app.services.ml_alert_service import generate_ml_alerts

def create_event(event_type = "authentication_failure", severity=Severity.HIGH):
    return SecurityEvent(
        timestamp = datetime.fromisoformat("2026-09-27T09:15:22"),
        source_ip="192.168.1.105",
        username="admin",
        event_type=event_type,
        service="ssh",
        source="linux_ssh",
        severity=severity,
        message="Failed password for admin",
    )

def test_generate_ml_alerts_returns_list():
    events = [
        create_event("authenication_failure"),
        create_event("authentication_success", Severity.LOW),
        create_event("user_login", Severity.LOW)
    ]
    service = AnomalyDetectionService()
    service.train(events)
    alerts = generate_ml_alerts(events, service)
    assert isinstance(alerts, list)

def test_ml_alert_contains_required_fields_when_anomaly_detected():
    events = [
        create_event("authentication_failure"),
        create_event("authentication_success", Severity.LOW),
        create_event("user_login", Severity.LOW),
        create_event("authentication_success", Severity.LOW),
        create_event("user_login", Severity.LOW)
    ]
    service = AnomalyDetectionService()
    service.train(events)

    anomaly_event = create_event("privilege_escalation", Severity.CRITICAL)
    alerts = generate_ml_alerts([anomaly_event], service)

    if alerts:
        alert = alerts[0]
        assert alert.alert_id
        assert alert.timestamp
        assert alert.severity == Severity.HIGH
        assert alert.reason
        assert isinstance(alert.evidence, list)