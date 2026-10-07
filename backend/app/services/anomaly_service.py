from app.detection.anomaly import AnomalyDetector
from app.models.schemas import SecurityEvent

class AnomalyDetectionService:
    """
    Service responsible for training and running the ML anomaly detection model.
    """

    def __init__(self):
        self.detector = AnomalyDetector()

    def train(self, events: list[SecurityEvent]) -> None:
        """
        Train the anomaly detection model..
        """
        self.detector.train(events)

    def analyze(self, event: SecurityEvent) -> dict:
        """
        Analyze a single security event and return its anomaly result.
        """
        result = self.detector.predict(event)
        return {
            "event_type": event.event_type,
            "source_ip": event.source_ip,
            "username": event.username,
            "is_anomaly": result["is_anomaly"],
            "anomaly_score": result["anomaly_score"],
            "risk_score" : result["risk_score"]
        }