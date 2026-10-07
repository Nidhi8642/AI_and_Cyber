import json
from pathlib import Path
from typing import Any
from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from app.ingestion.parser import parse_log
from app.ingestion.normalizer import normalize_log
from app.services.ingestion_service import process_logs
from app.services.alert_service import generate_alerts
from app.services.detection_service import DetectionService
from app.models.schemas import SecurityEvent
from app.services.dashboard_service import add_events, add_alerts

router = APIRouter(
    prefix ="/ingest",
    tags=["Ingestion"]
)

detection_service = DetectionService()

def train_detection_model():
    """
    Train the ML anomaly detection model using the sample security logs.
    """
    sample_file = (
        Path(__file__).parent.parent.parent
        / "sample_data"
        / "training_logs.json"
    )
    with open (sample_file, "r", encoding="utf-8") as file:
        raw_logs = json.load(file)

    events = process_logs(raw_logs)
    detection_service.train_model(events)

train_detection_model()

@router.post("/")
def ingest_log(raw_log: dict[str,Any]):
    if "timestamp" not in raw_log:
        raise HTTPException(status_code=400, detail="Missing required field: timestamp")

    parsed_log =  parse_log(raw_log)

    try:
        security_event = normalize_log(parsed_log)
    except ValidationError:
        raise HTTPException(status_code=400, detail="Invalid timestamp format")

    alerts = generate_alerts([security_event])
    add_events([security_event])
    add_alerts(alerts)
    ml_result = detection_service.anomaly_service.analyze(security_event)

    return{
        "message": "Log ingested successfully",
        "event": security_event,
        "alerts": alerts,
        "ml_alert" : ml_result
    }

@router.post("/batch")
def ingest_batch(raw_logs: list[dict[str,Any]]):
    if not raw_logs:
        raise HTTPException(status_code=400, detail="Log batch cannot be empty")

    for raw_log in raw_logs:
        if "timestamp" not in raw_log:
            raise HTTPException(status_code=400, detail="Missing required field: timestamp")

    try:
        events = process_logs(raw_logs)
    except ValidationError:
        raise HTTPException(status_code=400, detail="Invalid timestamp format.")

    detection_result = detection_service.detect(events)
    add_events(events)
    add_alerts(detection_result["rule_alerts"])
    add_alerts(detection_result["anomaly_alerts"])

    return {
        "message": "Log batch ingested successfully",
        "count": len(events),
        "events": events,
        "alerts": detection_result["rule_alerts"],
        "ml_alerts": detection_result["ml_alerts"],
        "anomaly_alerts" : detection_result["anomaly_alerts"]
    }

@router.post("/analyze")
def analyze_event(event: SecurityEvent):
    return detection_service.anomaly_service.analyze(event)