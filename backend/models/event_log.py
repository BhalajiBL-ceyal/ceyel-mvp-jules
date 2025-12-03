from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Any

class Event(BaseModel):
    case_id: str
    activity_name: str
    timestamp: datetime
    details: Dict[str, Any] = {}

class EventLog(BaseModel):
    events: List[Event]
