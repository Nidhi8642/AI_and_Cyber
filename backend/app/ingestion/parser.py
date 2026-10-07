from typing import Any

def parse_log(raw_log: dict[str,Any]) -> dict[str,Any]:
    """
    PArse a raw security log into a structured dictionary.
    """

    return{
        "timestamp": raw_log.get("timestamp"),
        "source_ip": raw_log.get("source_ip"),
        "username": raw_log.get("username"),
        "event": raw_log.get("event"),
        "service": raw_log.get("service"),
        "source": raw_log.get("source"),
        "message": raw_log.get("message")
    }