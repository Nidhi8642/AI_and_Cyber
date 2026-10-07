from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_batch_ingestion_rule_and_ml_results():
    logs = [
        {
            "timestamp":"2026-09-27T09:15:04",
            "source_ip" : "192.168.1.105",
            "username" : "admin",
            "event" : "Failed password",
            "service" : "ssh",
            "source" : "linux_ssh",
            "message" : "Failed password for admin"
        },
        {
            "timestamp":"2026-09-27T09:17:44",
            "source_ip" : "192.168.1.105",
            "username" : "admin",
            "event" : "Failed password",
            "service" : "ssh",
            "source" : "linux_ssh",
            "message" : "Failed password for admin"
        },
        {
            "timestamp":"2026-09-27T09:19:54",
            "source_ip" : "192.168.1.105",
            "username" : "admin",
            "event" : "Failed password",
            "service" : "ssh",
            "source" : "linux_ssh",
            "message" : "Failed password for admin"
        },
        {
            "timestamp":"2026-09-27T09:21:15",
            "source_ip" : "192.168.1.105",
            "username" : "admin",
            "event" : "Failed password",
            "service" : "ssh",
            "source" : "linux_ssh",
            "message" : "Failed password for admin"
        }
    ]
    response = client.post("/ingest/batch", json=logs)

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == 4

    assert "events" in data
    assert "alerts" in data
    assert "ml_alerts" in data
    assert "anomaly_alerts" in data

    assert len(data["events"]) == 4
    assert isinstance(data["alerts"], list)
    assert isinstance(data["ml_alerts"], list)
    assert isinstance(data["anomaly_alerts"], list)

    for result in data["ml_alerts"]:
        assert "is_anomaly" in result
        assert "anomaly_score" in result
        assert "risk_score" in result
        assert isinstance(result["risk_score"], float)
        assert 0.0 <= result["risk_score"] <= 100.0

def test_analyze_endpoint_returns_risk_score():
    event = {
            "timestamp":"2026-09-27T09:15:04",
            "source_ip" : "192.168.1.105",
            "username" : "admin",
            "event_type" : "authentication_failure",
            "service" : "ssh",
            "source" : "linux_ssh",
            "severity": "high",
            "message" : "Failed password for admin"
        }
    response = client.post("/ingest/analyze", json=event)
    assert response.status_code == 200
    data = response.json()

    assert data["event_type"] == "authentication_failure"
    assert "risk_score" in data
    assert 0.0 <= data["risk_score"] <= 100.0