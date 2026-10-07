from uuid import uuid4
from app.detection.rules import run_detection_rules
from app.models.schemas import Alert, SecurityEvent, Severity

def generate_alerts(events: list[SecurityEvent]) -> list[Alert]:
    """
    Run detection riles and convert detected threats into structured Alert objects.
    """

    alerts = []
    detection_results = run_detection_rules(events)

    for result in detection_results:
        if "Privilege escalation detected" in result:
            matching_event = next(
                (
                    event 
                                    for event in events
                                    if event.event_type == "privilege_escalation" 
                ),
                None
            )

            if matching_event:
                alerts.append(
                    Alert(
                        alert_id=str(uuid4()),
                        timestamp=matching_event.timestamp,
                        severity=Severity.CRITICAL,
                        reason="Privilege escalation detected",
                        evidence=[matching_event.message or "Privilege escalation event detected"],
                    )
                )

        elif "Possible brute-force attack detected" in result:
            source_ip = None

            for event in events:
                if event.event_type == "authentication_failure" and event.source_ip:
                    source_ip = event.source_ip
                    break

            evidence = [
                event.message or "Authentication failure."
                for event in events
                if (event.event_type == "authentication_failure" and event.source_ip == source_ip)
            ]

            alerts.append(
            Alert(
                alert_id=str(uuid4()),
                timestamp=events[0].timestamp,
                severity=Severity.HIGH,
                reason=result,
                evidence=evidence,
            )
        )

    return alerts