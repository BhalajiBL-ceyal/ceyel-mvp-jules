from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from backend.services.ingestion_service import ingestion_service
from backend.models.event_log import EventLog

router = APIRouter()

@router.post("/ingest/csv", response_model=EventLog)
async def ingest_csv(file: UploadFile = File(...)):
    """
    Ingests an event log from a CSV file.
    The CSV must contain 'case_id', 'activity_name', and 'timestamp' columns.
    """
    if file.content_type != 'text/csv':
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV.")
    try:
        event_log = await ingestion_service.process_csv(file)
        return event_log
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing CSV file: {e}")

@router.post("/ingest/api", response_model=EventLog)
async def ingest_api(events: List[dict]):
    """
    Ingests an event log from a JSON payload.
    The payload should be a list of event objects, each with 'case_id', 
    'activity_name', and 'timestamp'.
    """
    try:
        event_log = ingestion_service.process_api_payload(events)
        return event_log
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing API payload: {e}")
