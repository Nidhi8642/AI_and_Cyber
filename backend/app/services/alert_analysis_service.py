from app.services.ai_assistant_service import build_security_prompt

def analyze_alert(alert) -> dict:
    event_type = "security_alert"
    severity = alert.severity.value
    message = alert.reason
    result = build_security_prompt(event_type=event_type, severity=severity, message=message)
    return{
        "alert_id" : alert.alert_id,
        "severity" : severity,
        "analysis_prompt" : result["prompt"],
        "analysis" : result["analysis"],
        "knowledge" : result["knowledge"]
    }