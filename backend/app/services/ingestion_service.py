from typing import Any
from app.ingestion.parser import parse_log
from app.ingestion.normalizer import normalize_log
from app.models.schemas import SecurityEvent

def process_logs(raw_logs: list[dict[str,Any]]) -> list[SecurityEvent]:
    """
    Parse and normalize multiple raw security logs.
    """
    normalized_events = []

    for raw_log in raw_logs:
        parsed_log = parse_log(raw_log)
        event = normalize_log(parsed_log)
        normalized_events.append(event)

    return normalized_events