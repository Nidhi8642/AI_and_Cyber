from app.models.schemas import Alert, SecurityEvent

events_store: list[SecurityEvent] = []
alerts_store: list[Alert] = []

def add_events(events: list[SecurityEvent]) -> None:
    events_store.extend(events)

def add_alerts(alerts: list[Alert]) -> None:
    alerts_store.extend(alerts)

def get_summary() -> dict:
    critical_alerts = sum(
        1
        for alert in alerts_store
        if alert.severity.value == "critical"
    )

    return {
        "total_events" : len(events_store),
        "open_alerts" : sum(
            1
            for alert in alerts_store
            if alert.status == "open"
        ),
        "critical_alerts" : critical_alerts,
        "ml_anomalies" : sum(
            1
            for alert in alerts_store
            if "ML anomaly" in alert.reason
        )
    }

def get_recent_events(limit:int =10) -> list[SecurityEvent]:
    return events_store[-limit:][::-1]

def get_recent_alerts(limit: int = 10) -> list[Alert]:
    return alerts_store[-limit:][::-1]