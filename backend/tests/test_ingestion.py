import json
from fastapi.testclient import TestClient
from app.main import app
from app.ingestion.parser import parse_log
from app.ingestion.normalizer import normalize_log
from app.services.ingestion_service import process_logs
from pathlib import Path

client = TestClient(app)

def test_failed_login_normalization():
    raw_log = {
        "timestamp": "2023-10-01T12:50:00Z",
        "source_ip": "192.168.1.10",
        "username":"admin",
        "event":"failed password",
        "service": "ssh",
        "message": "Failed password for admin from 192.168.1.10"
    }

    parsed_log = parse_log(raw_log)
    event = normalize_log(parsed_log)

    assert event.event_type == "authentication_failure"
    assert event.severity.value == "high"
    assert event.source_ip == "192.168.1.10"
    assert event.username == "admin"

def test_privilege_escalation_normalization():
    raw_log = {
        "timestamp": "2023-10-01T07:33:56Z",
        "source_ip": "192.168.1.20",
        "username": "root",
        "event": "Privilege escalation",
        "service": "system",
        "message": "User  root privilege escalation detected"
    }

    parsed_log = parse_log(raw_log)
    event = normalize_log(parsed_log)

    assert event.event_type == "privilege_escalation"
    assert event.severity.value == "critical"

def test_ingest_missing_timestamp():
    raw_log = {
        "source_ip": "192.168.1.10",
        "username": "admin",
        "event": "failed password",
        "service": "ssh",
        "message": "Failed password for admin."
    }

    response = client.post("/ingest/", json=raw_log)

    assert response.status_code == 400
    assert response.json()["detail"] == "Missing required field: timestamp"

def test_ingest_invalid_timestamp():
    raw_log = {
        "timestamp": "invalid-timestamp",
        "source_ip": "192.168.1.10",
        "username": "admin",
        "event": "failed password",
        "service": "ssh",
        "message": "Failed password for admin."
    }

    response = client.post("/ingest/", json=raw_log)

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid timestamp format"

def test_failed_login_variations():
    variations = [
        "Failed password",
        "Failed login",
        "Authentication failed",
        "Invalid password",
        "Login failed"
    ]

    for event_name in variations:
        raw_log = {
            "timestamp": "2023-10-01T11:55:32Z",
            "source_ip": "192.168.1.101",
            "username": "admin",
            "event": event_name,
            "service": "ssh",
            "message": f"Failed {event_name} for admin."
        }

        parsed_log = parse_log(raw_log)
        event = normalize_log(parsed_log)

        assert event.event_type == "authentication_failure"
        assert event.severity.value == "high"

def test_successful_login_variations():
    variations = [
        "Login successful",
        "Successful login",
        "Authentication successful",
        "Login accepted"
    ]

    for event_name in variations:
        raw_log = {
            "timestamp": "2023-10-01T17:05:12Z",
            "source_ip": "192.168.1.1",
            "username": "john_doe",
            "event": event_name,
            "service": "ssh",
            "message": f"{event_name} for john_doe."
        }

        parsed_log = parse_log(raw_log)
        event = normalize_log(parsed_log)

        assert event.event_type == "authentication_success"
        assert event.severity.value == "low"

def test_process_multiple_logs():
    raw_logs = [
        {
            "timestamp": "2023-10-01T19:32:06Z",
            "source_ip": "192.168.1.101",
            "username": "admin",
            "event": "failed password",
            "service": "ssh",
            "message": "Failed password for admin."
        },
        {
            "timestamp": "2023-10-01T17:41:10Z",
            "source_ip": "192.168.1.1",
            "username": "john_doe",
            "event": "Login successful",
            "service": "ssh",
            "message": "Login successful for john_doe."
        }
    ]

    events = process_logs(raw_logs)

    assert len(events) == 2
    assert events[0].event_type == "authentication_failure"
    assert events[1].event_type == "authentication_success"

def test_batch_ingestion_api():
    raw_logs = [
        {
            "timestamp": "2023-10-01T19:32:06Z",
            "source_ip": "192.168.1.101",
            "username": "admin",
            "event": "failed password",
            "service": "ssh",
            "message": "Failed password for admin."
        },
        {
            "timestamp": "2023-10-01T17:41:10Z",
            "source_ip": "192.168.1.1",
            "username": "john_doe",
            "event": "Login successful",
            "service": "ssh",
            "message": "Login successful for john_doe."
        }
    ]

    response = client.post("/ingest/batch", json=raw_logs)

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == 2
    assert len(data["events"]) == 2
    assert data["events"][0]["event_type"] == "authentication_failure"
    assert data["events"][1]["event_type"] == "authentication_success"

def test_sample_logs_processing():
    sample_file = (Path(__file__).parent.parent / "sample_data" / "raw_logs.json")
    with open(sample_file, "r", encoding="utf-8") as file:
        raw_logs = json.load(file)

    events = process_logs(raw_logs)

    assert len(events) == 5
    assert events[0].event_type == "authentication_failure"
    assert events[1].event_type == "authentication_failure"
    assert events[2].event_type == "authentication_success"
    assert events[3].event_type == "user_login"
    assert events[4].event_type == "privilege_escalation"

    assert events[0].severity.value == "high"
    assert events[4].severity.value == "critical"

    assert events[0].source == "linux_ssh"
    assert events[2].source == "linux_ssh"
    assert events[3].source == "web_application"
    assert events[4].source == "linux_system"

def test_ingest_generates_privilege_alert():
    raw_log = {
        "timestamp": "2023-10-01T07:33:56Z",
        "source_ip": "192.168.1.200",
        "username": "root",
        "event": "privilege escalation",
        "service": "linux_system",
        "message": "User root privilege escalation detected."
    }

    response = client.post("/ingest/", json=raw_log)

    assert response.status_code == 200

    data = response.json()

    assert data["event"]["event_type"] == "privilege_escalation"
    assert len(data["alerts"]) == 1
    assert data["alerts"][0]["severity"] == "critical"
    assert data["alerts"][0]["reason"] == "Privilege escalation detected"
    assert len(data["alerts"][0]["evidence"]) > 0

def test_batch_ingest_generates_brute_force_alert():
    raw_logs = [
        {
            "timestamp": "2023-10-01T12:43:10Z",
            "source_ip": "192.168.1.105",
            "username": "admin",
            "event": "Failed password",
            "service": "ssh",
            "source": "linux_ssh",
            "message": "Failed password for admin."
        },
        {
            "timestamp": "2023-10-01T12:45:15Z",
            "source_ip": "192.168.1.105",
            "username": "admin",
            "event": "Failed password",
            "service": "ssh",
            "source": "linux_ssh",
            "message": "Failed password for admin."
        },
        {
            "timestamp": "2023-10-01T12:47:20Z",
            "source_ip": "192.168.1.105",
            "username": "admin",
            "event": "Failed password",
            "service": "ssh",
            "source": "linux_ssh",
            "message": "Failed password for admin."
        }
    ]

    response = client.post("/ingest/batch", json=raw_logs)

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == 3
    assert len(data["events"]) == 3
    assert len(data["alerts"]) == 1
    assert data["alerts"][0]["severity"] == "high"
    assert "brute-force" in data["alerts"][0]["reason"]
    assert len(data["alerts"][0]["evidence"]) == 3