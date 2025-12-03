from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.models.event_log import EventLog
from backend.models.process_model import ProcessModel
from backend.models.conformance_result import ConformanceResult
from backend.services.conformance_service import conformance_service

router = APIRouter()

class ConformanceCheckRequest(BaseModel):
    event_log: EventLog
    process_model: ProcessModel

@router.post("/conformance/check", response_model=ConformanceResult)
async def check_conformance(request: ConformanceCheckRequest):
    """
    Performs conformance checking on an event log against a process model.
    """
    try:
        result = conformance_service.check_conformance(
            model=request.process_model,
            log=request.event_log
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during conformance checking: {e}")
