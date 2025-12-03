from fastapi import FastAPI
from backend.api import ingestion, process_discovery, conformance

app = FastAPI(
    title="CEYEL MVP",
    description="API for the CEYEL Process Mining Platform",
    version="0.1.0"
)

app.include_router(ingestion.router, prefix="/api/v1", tags=["Ingestion"])
app.include_router(process_discovery.router, prefix="/api/v1", tags=["Process Discovery"])
app.include_router(conformance.router, prefix="/api/v1", tags=["Conformance Checking"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the CEYEL API"}
