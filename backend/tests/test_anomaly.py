from datetime import datetime
import pytest
from app.models.schemas import SecurityEvent, Severity
from app.detection.anomaly import AnomalyDetector

def create_event(event_type: str, severity: Severity, source_ip: str = "192.168.1.105") -> SecurityEvent:
    return SecurityEvent(
        timestamp=datetime.fromisoformat("2026-01-01T20:40:11"),
        source_ip=source_ip,
        username="admin",
        event_type=event_type,
        service="ssh",
        source="linux_ssh",
        severity=severity,
        message="Test security event"       
    )

def test_anomaly_detector_requires_training():
    detector = AnomalyDetector()
    event = create_event("authentication_failure", Severity.HIGH)

    with pytest.raises(RuntimeError):
        detector.predict(event)

def test_anomaly_detector_can_train():
    detector = AnomalyDetector()
    events = [
        create_event("authentication_success", Severity.LOW),
        create_event("authentication_success", Severity.LOW),
        create_event("user_login", Severity.LOW),
        create_event("authentication_failure", Severity.HIGH),
        create_event("authentication_failure", Severity.HIGH)
    ]

    detector.train(events)
    assert detector.is_trained is True

def test_anomaly_detector_returns_prediction():
    detector = AnomalyDetector()
    training_events = [
        create_event("authentication_success", Severity.LOW),
        create_event("authentication_success", Severity.LOW),
        create_event("user_login", Severity.LOW),
        create_event("authentication_failure", Severity.HIGH),
        create_event("authentication_failure", Severity.HIGH)
    ]

    detector.train(training_events)

    event = create_event("authentication_failure", Severity.HIGH)
    result = detector.predict(event)

    assert "is_anomaly" in result
    assert "anomaly_score" in result
    assert isinstance(result["is_anomaly"], bool)
    assert isinstance(result["anomaly_score"], float)