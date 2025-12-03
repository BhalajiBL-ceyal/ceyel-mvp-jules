import pandas as pd
from typing import List
from fastapi import UploadFile
from io import StringIO
from backend.models.event_log import Event, EventLog

class IngestionService:
    def normalize_log(self, df: pd.DataFrame) -> EventLog:
        """
        Normalizes a pandas DataFrame into an EventLog object.
        Assumes standard column names: 'case_id', 'activity_name', 'timestamp'.
        All other columns are stored in the 'details' dictionary.
        """
        events = []
        required_columns = ['case_id', 'activity_name', 'timestamp']
        for index, row in df.iterrows():
            # Ensure required columns are present
            if not all(col in row for col in required_columns):
                raise ValueError(f"Row {index} is missing one of the required columns: {required_columns}")

            # Convert timestamp
            try:
                timestamp = pd.to_datetime(row['timestamp'])
            except Exception as e:
                raise ValueError(f"Could not parse timestamp in row {index}: {e}")

            # Collect other details
            details = {key: val for key, val in row.items() if key not in required_columns}

            events.append(Event(
                case_id=str(row['case_id']),
                activity_name=str(row['activity_name']),
                timestamp=timestamp,
                details=details
            ))
        return EventLog(events=events)

    async def process_csv(self, file: UploadFile) -> EventLog:
        """
        Processes an uploaded CSV file, normalizes it, and returns an EventLog.
        """
        content = await file.read()
        csv_file = StringIO(content.decode('utf-8'))
        df = pd.read_csv(csv_file)
        return self.normalize_log(df)

    def process_api_payload(self, events_data: List[dict]) -> EventLog:
        """
        Processes a list of event dictionaries from an API call, normalizes it,
        and returns an EventLog.
        """
        df = pd.DataFrame(events_data)
        return self.normalize_log(df)

ingestion_service = IngestionService()
