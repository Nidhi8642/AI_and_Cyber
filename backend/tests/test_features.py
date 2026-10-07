from datetime import datetime
from app.models.schemas import SecurityEvent, Severity
from app.detection.features import extract_features

def test_authentication_failure_features():
    event = SecurityEvent(
        timestamp=datetime.fromisoformat("2026-06-01T12:43:10"),
        source_ip="192.168.1.105",
        username="admin",
        event_type="authentication_failure",
        service="ssh",
        source="linux_ssh",
        severity=Severity.HIGH,
        message="Failed password for admin."
    )

    features = extract_features(event)

    assert features == [1.0, 3.0, 1.0, 1.0, 1.0]

def test_privilege_escalation_features():
    event = SecurityEvent(
        timestamp=datetime.fromisoformat("2026-06-01T11:30:00"),
        source_ip="192.168.1.200",
        username="root",
        event_type="privilege_escalation",
        service="system",
        source="linux_system",
        severity=Severity.CRITICAL,
        message="User root privilege escalation detected."
    )

    features = extract_features(event)

    assert features == [4.0, 4.0, 1.0, 1.0, 1.0]

def test_missing_optional_fields():
    event = SecurityEvent(
        timestamp=datetime.fromisoformat("2026-06-01T10:00:00"),
        event_type="authentication_success",
        service=None,
        severity=Severity.LOW
    )

    features = extract_features(event)

    assert features == [2.0, 1.0, 0.0, 0.0, 0.0]