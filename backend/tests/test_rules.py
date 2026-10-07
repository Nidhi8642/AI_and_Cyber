from datetime import datetime
from app.detection.rules import (detect_privilege_escalation, detect_brute_force, run_detection_rules)
from app.models.schemas import SecurityEvent, Severity

def test_privilege_escalation_detection():
    event = SecurityEvent(
        timestamp=datetime.fromisoformat("2023-10-01T07:33:56"),
        source_ip="192.168.1.105",
        username="root",
        event_type="privilege_escalation",
        service="system",
        source="linux_system",
        severity=Severity.CRITICAL,
        message="User root privilege escalation detected."
    )
    result = detect_privilege_escalation(event)
    assert result == "Privilege escalation detected"

def test_normal_login_not_privilege_escalation():
    event = SecurityEvent(
        timestamp=datetime.fromisoformat("2023-10-01T12:50:00"),
        source_ip="192.168.1.106",
        username="john",
        event_type="authentication_success",
        service="ssh",
        source="linux_ssh",
        severity=Severity.LOW,
        message="Accepted password for john."
    )
    result = detect_privilege_escalation(event)
    assert result is None

def test_brute_force_detected():
    events = []

    for _ in range(3):
        events.append(
            SecurityEvent(
                timestamp=datetime.fromisoformat("2026-09-27T09:15:22"),
                source_ip="192.168.1.105",
                username="admin",
                event_type="authentication_failure",
                service="ssh",
                source="linux_ssh",
                severity=Severity.HIGH,
                message="Failed password for admin"
            )
        )
    result = detect_brute_force(events)

    assert result is not None
    assert "192.168.1.105" in result
    assert " 3 failed authentication attempts" in result

def test_brute_force_not_detected_below_threshold():
    events = []
    for _ in range(2):
            events.append(
                SecurityEvent(
                    timestamp=datetime.fromisoformat("2026-09-27T09:16:45"),
                    source_ip="192.168.1.105",
                    username="admin",
                    event_type="authentication_failure",
                    service="ssh",
                    source="linux_ssh",
                    severity=Severity.HIGH,
                    message="Failed password for admin"
                ),

            )
    result =  detect_brute_force(events)
    assert result is None

def test_run_detection_rules():
    events = [
        SecurityEvent(
            timestamp=datetime.fromisoformat("2026-10-01T07:33:56"),
            source_ip="192.168.1.105",
            username="root",
            event_type="privilege_escalation",
            service="system",
            source="linux_system",
            severity=Severity.CRITICAL,
            message="User root privilege escalation detected."
        ),
        SecurityEvent(
            timestamp=datetime.fromisoformat("2026-09-27T09:15:22"),
            source_ip="192.168.1.105",
            username="admin",
            event_type="authentication_failure",
            service="ssh",
            source="linux_ssh",
            severity=Severity.HIGH,
            message="Failed password for admin"
        ),
        SecurityEvent(
            timestamp=datetime.fromisoformat("2026-09-27T09:15:22"),
            source_ip="192.168.1.105",
            username="admin",
            event_type="authentication_failure",
            service="ssh",
            source="linux_ssh",
            severity=Severity.HIGH,
            message="Failed password for admin"
        ),
        SecurityEvent(
            timestamp=datetime.fromisoformat("2026-09-27T09:15:22"),
            source_ip="192.168.1.105",
            username="root",
            event_type="authentication_failure",
            service="ssh",
            source="linux_ssh",
            severity=Severity.HIGH,
            message="Failed password for root"
        ),
    ]

    alerts = run_detection_rules(events)
    assert len(alerts) == 2
    assert "Privilege escalation detected" in alerts[0]
    assert "Possible brute-force attack detected" in alerts[1]
