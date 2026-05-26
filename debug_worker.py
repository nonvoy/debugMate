from typing import Any

from pydantic import ValidationError

from src.config.basic_config import get_config
from src.routes.schemas.events import EventGet, Severity
from src.services.celery.client import get_celery_client


config = get_config()
celery_app = get_celery_client()


def _normalize_event_payload(event_payload: dict[str, Any]) -> EventGet:
    """Validate task input against the same schema returned by the API."""
    return EventGet.model_validate(event_payload)


def _build_debug_report(event: EventGet) -> dict[str, Any]:
    findings: list[str] = []

    if event.severity in {Severity.error, Severity.critical}:
        findings.append("Event severity requires investigation.")

    if not event.environment:
        findings.append("Event is missing environment context.")

    if not event.event_type:
        findings.append("Event is missing event_type context.")

    if not event.metadata:
        findings.append("Event has no metadata for correlation.")

    return {
        "event_id": str(event.id),
        "batch_id": str(event.batch_id) if event.batch_id else None,
        "service": event.service,
        "severity": event.severity.value,
        "environment": event.environment,
        "event_type": event.event_type,
        "timestamp": event.timestamp.isoformat(),
        "requires_attention": event.severity in {Severity.error, Severity.critical},
        "findings": findings,
    }


@celery_app.task(name=config.celery.task_name, bind=True)
def debug_endpoint(self, event_payload: dict[str, Any]) -> dict[str, Any]:
    """
    Process event payloads emitted by the /events endpoint and return a debug report.

    Run with:
        celery -A debug_worker.celery_app worker --loglevel=info
    """
    try:
        event = _normalize_event_payload(event_payload)
    except ValidationError as exc:
        return {
            "status": "invalid_event",
            "task_id": self.request.id,
            "errors": exc.errors(),
        }

    return {
        "status": "debugged",
        "task_id": self.request.id,
        "report": _build_debug_report(event),
    }
