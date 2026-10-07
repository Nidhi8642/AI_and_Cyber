from datetime import datetime
import pytest
from app.models.schemas import SecurityEvent, Severity
from app.services.anomaly_service import AnomalyDetectionService
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def create_event(event_type: str,severity: Severity) -> SecurityEvent:
    return SecurityEvent(
        timestamp=datetime.fromisoformat("2026-01-01T13:10:00"),
        source_ip="192.168.1.105",
        username="admin",
        event_type=event_type,
        service="ssh",
        source="linux_ssh",
        severity=severity,
        message="Test security event"
    )

def test_service_requires_training():
    service = AnomalyDetectionService()
    event = create_event("authentication_failure", Severity.HIGH)
    
    with pytest.raises(RuntimeError):
        service.analyze(event)

def test_service_can_train_and_analyze():
    service = AnomalyDetectionService()
    training_events = [
        create_event("authentication_success", Severity.LOW),
        create_event("authentication_success", Severity.LOW),
        create_event("user_login", Severity.LOW),
        create_event("authentication_failure", Severity.HIGH),
        create_event("authentication_failure", Severity.HIGH)
    ]
    
    service.train(training_events)
    
    result = service.analyze(training_events[0])
    
    assert result ["event_type"] == "authentication_success"
    assert result["source_ip"] == "192.168.1.105"
    assert result["username"] == "admin"
    assert isinstance(result["is_anomaly"], bool)
    assert isinstance(result["anomaly_score"], float)

def test_analyze_event_api():
    event = {
        "timestamp" : "2026-09-27T09:15:22",
        "source_ip" : "192.168.1.105",
        "username" : ":admin",
        "event_type" : "authentication_failure",
        "service" : "ssh",
        "source" : "linux_ssh",
        "severity" : "high",
        "message" : "Failed password for admin"
    }

    response = client.post("/ingest/analyze", json = event)

    assert response.status_code == 200

    data = response.json()

    assert "event_type" in data
    assert "source_ip" in data
    assert "username" in data
    assert "is_anomaly" in data
    assert "anomaly_score" in data
    assert "risk_score" in data
    assert isinstance(data["risk_score"], float)
    assert 0.0 <= data["risk_score"] <= 100.0

    assert data["event_type"] == "authentication_failure"
    assert isinstance(data["is_anomaly"], bool)
    assert isinstance(data["anomaly_score"], float)