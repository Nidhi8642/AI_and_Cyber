from app.models.schemas import SecurityEvent

def detect_privilege_escalation(event: SecurityEvent) -> str |None:
    """
    Detect privilege escalation events
    Returns an alert reason if detected, otherwise None.
    """

    if event.event_type == "privilege_escalation":
        return "Privilege escalation detected"
    return None

def detect_brute_force(events: list[SecurityEvent], threshold: int = 3) -> str | None:
    """
    Detect repeated authentication failures from the same source IP.
    """

    failed_attempts: dict[str, int] = {}

    for event in events:
        if(event.event_type == "authentication_failure" and event.source_ip):
            failed_attempts[event.source_ip] = (failed_attempts.get(event.source_ip, 0) + 1)

    for source_ip, count in failed_attempts.items():
        if count >= threshold:
            return (
                f"Possible brute-force attack detected "
                f"{source_ip}: {count} failed authentication attempts"
            )
    return None
def run_detection_rules(events: list[SecurityEvent]) -> list[str]:
    """
    Run all detection rules against a collection of security events.
    Returns a list of detected alerts.
    """

    alerts = []

#Rule 1: Privilege escalation
    for event in events:
        result = detect_privilege_escalation(event)
        if result:
            alerts.append(result)

    brute_force_result = detect_brute_force(events)
    if brute_force_result:
        alerts.append(brute_force_result)

    return alerts