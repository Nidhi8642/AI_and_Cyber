from app.models.schemas import SecurityEvent
from app.services.alert_service import generate_alerts
from app.services.anomaly_service import AnomalyDetectionService
from app.services.ml_alert_service import generate_ml_alerts

class DetectionService:
    """
    Combine rule based detection and ML based anomaly detection.
    """

    def __init__(self):
        self.anomaly_service = AnomalyDetectionService()

    def train_model(self, events: list[SecurityEvent]) -> None:
        """
        Train the ML anomaly model.
        """
        self.anomaly_service.train(events)

    def detect(self, events: list[SecurityEvent]) -> dict:
        """
        Run both rule based and ML based detection.
        """

        rule_alerts = generate_alerts(events)
        ml_alerts = []

        for event in events:
            result = self.anomaly_service.analyze(event)
            ml_alerts.append(result)

        anomaly_alerts =  generate_ml_alerts(events, self.anomaly_service)

        return {
            "rule_alerts": rule_alerts,
            "ml_alerts": ml_alerts,
            "anomaly_alerts" : anomaly_alerts
        }