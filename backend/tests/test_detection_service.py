from datetime import datetime
from app.models.schemas import SecurityEvent, Severity
from app.services.detection_service import DetectionService

def create_event(event_type: str, severity: Severity, source_ip: str = "192.168.1.105") -> SecurityEvent:
    return SecurityEvent(
        timestamp=datetime.fromisoformat("2026-01-01T05:43:36"),
        source_ip=source_ip,
        username="admin",
        event_type=event_type,
        service="ssh",
        source = "linux_ssh",
        severity=severity,
        message = "Test security event"
    )

def test_detection_service_combines_rules_and_ml():
    service = DetectionService()

    training_events = [
        create_event("authentication_success", Severity.LOW),
        create_event("authentication_success", Severity.LOW),
        create_event("user_login", Severity.LOW),
        create_event("authentication_failure", Severity.HIGH),
        create_event("authentication_failure", Severity.HIGH),
    ]

    service.train_model(training_events)

    events = [
        create_event("privilege_escalation", Severity.CRITICAL, "192.168.1.200"),
        create_event("authentication_failure", Severity.HIGH),
        create_event("authentication_failure", Severity.HIGH),
        create_event("authentication_failure", Severity.HIGH)
    ]

    result = service.detect(events)

    assert "rule_alerts" in result
    assert "ml_alerts" in result

    assert len(result["rule_alerts"]) == 2
    assert len(result["ml_alerts"]) == 4

    assert result["rule_alerts"][0].severity == Severity.CRITICAL
    assert result["rule_alerts"][1].severity == Severity.HIGH

    for ml_result in result["ml_alerts"]:
        assert "is_anomaly" in ml_result
        assert "anomaly_score" in ml_result