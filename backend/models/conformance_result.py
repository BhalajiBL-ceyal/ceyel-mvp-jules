from pydantic import BaseModel
from typing import List, Dict, Any

class Deviation(BaseModel):
    case_id: str
    activity_name: str
    deviation_type: str # e.g., "Missing", "Unexpected"
    timestamp: Any

class ConformanceResult(BaseModel):
    fitness: float
    deviations: List[Deviation]
