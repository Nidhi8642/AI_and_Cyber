from datetime import datetime
from app.models.schemas import SecurityEvent, Severity
from app.services.alert_service import generate_alerts

def test_generate_alerts_privilege_escalation_alert():
    events =[
        SecurityEvent(
            timestamp=datetime.fromisoformat("2026-06-01T12:00:00"),
            source_ip="192.168.1.200",
            username="root",
            event_type="privilege_escalation",
            service="system",
            source="linux_system",
            severity=Severity.CRITICAL,
            message="Privilege escalation detected."
        )
    ]

    alerts = generate_alerts(events)
    assert len(alerts) == 1
    assert alerts[0].severity == Severity.CRITICAL
    assert alerts[0].reason == "Privilege escalation detected"
    assert len(alerts[0].evidence) > 0
    assert alerts[0].status == "open"

def test_generate_alerts_brute_force_alert():
    events = []

    for _ in range(3):
        events.append(
            SecurityEvent(
                timestamp=datetime.fromisoformat("2026-06-01T12:43:10"),
                source_ip="192.168.1.105",
                username="admin",
                event_type="authentication_failure",
                service="ssh",
                source="linux_ssh",
                severity=Severity.HIGH,
                message="Failed password for admin."
            )
        )

    alerts = generate_alerts(events)
    assert len(alerts) == 1
    assert alerts[0].severity == Severity.HIGH
    assert "brute-force" in alerts[0].reason
    assert len(alerts[0].evidence) == 3
    assert alerts[0].status == "open"