import json
from pathlib import Path
from app.ingestion.normalizer import normalize_log
from app.ingestion.parser import parse_log
from app.services.anomaly_service import AnomalyDetectionService

def load_training_logs():
    training_file = (
        Path(__file__).parent.parent
        / "sample_data"
        / "training_logs.json"
    )
    with open(training_file, "r", encoding="utf-8") as file:
        return json.load(file)

def test_training_dataset_exists():
    logs = load_training_logs()
    assert isinstance(logs, list)
    assert len(logs) >= 10

def test_training_data_can_be_normalized():
    logs = load_training_logs()
    events =[
        normalize_log(parse_log(log))
        for log in logs
    ]
    assert len(events) == len(logs)

    for event in events:
        assert event.timestamp is not None
        assert event.event_type is not None

def test_anomaly_detector_can_train_on_dataset():
    logs = load_training_logs()
    events = [
        normalize_log(parse_log(log))
        for log in logs
    ]

    service = AnomalyDetectionService()
    service.train(events)

    assert service.detector.is_trained is True