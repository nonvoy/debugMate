import uuid

from fastapi import APIRouter, status, Depends

from src.routes.schemas.events import EventCreate, EventGet
from src.config.basic_config import get_config
from src.config.logger import get_logger
from src.services.celery.client import get_celery_client


config = get_config()
logger = get_logger(__name__)

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/", response_model=EventGet, status_code=status.HTTP_201_CREATED)
async def create_event(event: EventCreate, celery_app=Depends(get_celery_client)):
    """
    Create a new event and publish it to the Celery task queue for processing.

    This endpoint allows you to create a new event by providing the necessary details such as service name, severity, message, environment, event type, metadata, and timestamp.

    - **service**: The name of the service that generated the event (e.g., 'auth-service', 'payment-service').
    - **severity**: The severity level of the event (e.g., 'info', 'warning', 'error').
    - **message**: A descriptive message about the event (e.g., 'User login successful', 'Payment failed due to insufficient funds').
    - **environment**: (Optional)The environment where the event occurred (e.g., 'production', 'staging').
    - **event_type**: (Optional) The type of event (e.g., 'authentication', 'payment').
    - **metadata**: (Optional) Additional metadata related to the event (e.g., {'user_id': '12345', 'transaction_id': 'abcde'}).
    - **timestamp**: The timestamp when the event occurred in ISO 8601 format (e.g., '2024-06-01T12:00:00Z').

    Returns the created event with its unique identifier.
    """
    event_id = uuid.uuid4()
    created_event = EventGet(
        id=event_id,
        **event.model_dump()
    )
    celery_app.send_task(config.celery.task_name, task_id=str(event_id), args=[created_event.model_dump()])
    logger.info(f"Event created with ID: {event_id} and published to Celery task queue.")
    return created_event