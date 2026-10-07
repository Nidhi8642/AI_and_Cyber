from uuid import uuid4
from app.models.schemas import Alert, SecurityEvent, Severity
from app.services.anomaly_service import AnomalyDetectionService

def generate_ml_alerts(events: list[SecurityEvent], anomaly_service: AnomalyDetectionService) -> list[Alert]:
    alerts = []
    for event in events:
        result = anomaly_service.analyze(event)

        if result["is_anomaly"]:
            alerts.append(
                Alert(
                    alert_id=str(uuid4()),
                    timestamp=event.timestamp,
                    severity = Severity.HIGH,
                    reason = f"ML anomaly detected for {event.event_type} (score: {result['anomaly_score']:.4f})",
                    evidence=[event.message or "Anomalous security event detected"]
                    )
                )
    return alerts