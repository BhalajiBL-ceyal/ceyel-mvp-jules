from fastapi import APIRouter
from backend.models.event_log import EventLog
from backend.models.process_model import ProcessModel
from backend.services.process_discovery_service import dfg_discovery_service

router = APIRouter()

@router.post("/discover/dfg", response_model=ProcessModel)
async def discover_dfg(event_log: EventLog):
    """
    Discovers a process model using the Directly-Follows Graph (DFG) algorithm.
    """
    try:
        process_model = dfg_discovery_service.discover(event_log)
        return process_model
    except Exception as e:
        # In a real app, you'd have more specific error handling
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"An error occurred during process discovery: {e}")
