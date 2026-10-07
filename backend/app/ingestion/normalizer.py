from app.models.schemas import SecurityEvent, Severity

def normalize_log(parsed_log: dict) -> SecurityEvent:
    event = parsed_log.get("event", "").lower()

    if any(keyword in event for keyword in [
        "failed password",
        "failed login",
        "authentication failed",
        "invalid password",
        "login failed",
    ]):
        event_type = "authentication_failure"
        severity = Severity.HIGH

    elif any(keyword in event for keyword in [
        "login successful",
        "successful login",
        "authentication successful",
        "login accepted"
    ]):
        event_type = "authentication_success"
        severity = Severity.LOW

    elif any(keyword in event for keyword in [
        "user login",
        "user logged in",
        "account login"
    ]):
        event_type = "user_login"
        severity = Severity.LOW

    elif any(keyword in event for keyword in [
        "privilege escalation",
        "elevated privilege",
        "privilege elevation",
    ]):
        event_type = "privilege_escalation"
        severity = Severity.CRITICAL

    else:
        event_type = "unknown"
        severity = Severity.LOW

    return SecurityEvent(
        timestamp=parsed_log["timestamp"],
        source_ip=parsed_log.get("source_ip"),
        username=parsed_log.get("username"),
        event_type=event_type,
        service=parsed_log.get("service"),
        source=parsed_log.get("source"),
        severity=severity,
        message=parsed_log.get("message")
    )