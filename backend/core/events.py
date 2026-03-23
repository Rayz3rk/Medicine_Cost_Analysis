from typing import Any, Dict
import uuid
from datetime import datetime
from pydantic import BaseModel, Field

class CloudEvent(BaseModel):
    specversion: str = "1.0"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source: str
    type: str
    time: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    data_content_type: str = "application/json"
    data: Dict[str, Any]
    signature: str = ""

def create_event(source: str, event_type: str, data: dict) -> CloudEvent:
    event = CloudEvent(source=source, type=event_type, data=data)
    # Could add signature generation here based on data
    return event
