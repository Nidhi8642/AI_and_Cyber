from sklearn.ensemble import IsolationForest
from app. detection.features import extract_features
from app.models.schemas import SecurityEvent

class AnomalyDetector:
    """
    ML-based anomaly detector using Isolation Forest.
    """

    def __init__(self):
        self.model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
        self.is_trained = False

    def train(self, events: list[SecurityEvent]) -> None:
        """
        Train the anomaly detection model using security events.
        """

        if not events:
            raise ValueError("Cannot train model with no events.")
        
        features = [extract_features(event) for event in events]
        self.model.fit(features)
        self.is_trained = True

    def predict(self, event: SecurityEvent) -> dict:
        """
        Predict whether a security event is anomalous.
        """

        if not self.is_trained:
            raise RuntimeError("Anomaly detector has not been trained.")
        
        features = [extract_features(event)]
        prediction = self.model.predict(features)[0]
        score = self.model.decision_function(features)[0]
        risk_score = max(0.0, min(100.0, (0.5 - score) * 100))
        return {
            "is_anomaly": bool(prediction == -1),
            "anomaly_score": float(score),
            "risk_score" : round(risk_score, 2) 
        }