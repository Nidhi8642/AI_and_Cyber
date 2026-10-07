from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

class Severity(str,Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class SecurityEvent(BaseModel):
    timestamp: datetime
    source_ip: str | None = None
    username: str | None = None
    event_type: str
    service: str | None = None
    source: str | None = None
    severity: Severity = Severity.LOW
    message: str | None = None

class Alert(BaseModel):
    alert_id: str
    timestamp: datetime
    severity: Severity
    reason: str
    evidence: list[str]
    status: str ="open"