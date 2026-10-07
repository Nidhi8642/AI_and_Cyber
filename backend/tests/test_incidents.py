from app.services.incident_response_service import (create_incident_from_alert, update_incident_status)
from app.models.schemas import Alert, Severity
from datetime import datetime
import pytest

def sample_alert():
    return Alert(
        alert_id="test-alert-001",
        timestamp=datetime(2025,10,6,0,0),
        severity=Severity.HIGH,
        reason="Possible brute-force attack detected",
        evidence=[
            "Failed Authentication attempt",
            "Failed Authentication attempt",
            "Failed Authentication attempt"
        ]
    )

def test_create_incident():
    incident =  create_incident_from_alert(sample_alert())
    assert incident["alert_id"] == "test-alert-001"
    assert incident["status"] == "open"
    assert incident["identify"]["status"] == "completed"
    assert incident["investigate"]["status"] == "pending"

def test_update_incident_status():
    incident = {"incident_id" : "incident-001", "status" : "open"}
    updated = update_incident_status(incident, "investigating")
    assert updated["status"] == "investigating"

def test_invalid_incident_status():
    incident = {"incident_id" : "incident-001", "status" : "open"}
    with pytest.raises(ValueError):
        update_incident_status(incident, "invalid_status")

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_incident_api():
    response = client.post(
        "/incidents/create",
        json={
            "alert_id" : "test-alert-001",
            "timestamp" : "2026-10-06T10:00:00",
            "severity" : "high",
            "reason" : "Possible brute-force attack detected",
            "evidence" : [
                "Failed Authentication attempt",
                "Failed Authentication attempt",
            ],
            "status" : "open"
        }
    )
    assert response.status_code == 200
    data = response.json()

    assert data["alert_id"] == "test-alert-001"
    assert data["status"] == "open"
    assert data["identify"]["status"] == "completed"

def test_invalid_incident_status_api():
    response = client.put(
        "/incidents/test-alert-001/status",
        json = {"status":"invalid_status"}
    )
    assert response.status_code == 400

def test_empty_batch_registered():
    response = client.post("/ingest/batch", json =[])
    assert response.status_code == 400
    assert response.json()["detail"] == "Log batch cannot be empty"

def test_missing_timestamp_rejected():
    response = client.post(
        "/ingest/",
        json = {
            "source_ip" : "192.168.1.100",
            "username" : "admin",
            "event" : "Failed password",
            "service" : "ssh",
            "source" : "linux_ssh",
            "message" : "Failed password for admin"
        }
    )
    assert response.status_code == 400
    assert "timestamp" in response.json()["detail"].lower()

def test_invalid_timestamp_rejected():
    response = client.post(
        "/ingest/",
        json = {
            "timestamp" : "not-a-valid-timestamp",
            "source_ip" : "192.168.1.100",
            "username" : "admin",
            "event" : "Failed password",
            "service" : "ssh",
            "source" : "linux_ssh",
            "message" : "Failed password for admin"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid timestamp format"

def test_empty_incident_status_rejected():
    response = client.put(
        "/incidents/test-alert-001/status",
        json = {
            "status" : "",
        }
    )

def test_invalid_severity_rejected():
    response = client.post(
        "/incidents/create",
        json = {
            "alert_id" : "validation-test-001",
            "timestamp" : "2026-10-06T10:00:00",
            "severity" : "extreme",
            "reason" : "Test Alert",
            "evidence" : ["Test evidence"],
            "status" : "open"
        }
    )
    assert response.status_code == 422
