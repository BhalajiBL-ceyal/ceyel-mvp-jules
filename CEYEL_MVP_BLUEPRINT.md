# CEYEL - MVP Blueprint

**Version:** 0.1
**Date:** 2025-12-02
**Author:** JULES

---

## 1. MVP Scope

This document outlines the Minimum Viable Product (MVP) for CEYEL, an AI-driven process mining platform. The scope is strictly limited to the features required for a successful pilot deployment in a manufacturing environment.

### 1.1. Module Prioritization

| Module                      | Category  | Priority | Justification                                                                 |
| --------------------------- | --------- | -------- | ----------------------------------------------------------------------------- |
| **Event Log Ingestion**     | Core      | High     | Foundation of the system; without data, no analysis is possible.              |
| **Log Normalization**       | Core      | High     | Ensures data consistency for reliable process discovery.                      |
| **Process Discovery**       | Core      | High     | Generates the process model, which is the central artifact for analysis.      |
| **Conformance Checking**    | Core      | High     | Provides immediate value by identifying deviations from the discovered model. |
| **Dashboard & Visualizer**  | Core      | High     | The primary user interface for presenting insights and results.               |
| **API Layer**               | Core      | High     | Enables communication between the backend and frontend.                       |
| **Database**                | Core      | High     | Stores event logs, process models, and analysis results.                      |
| Cost/Time Analysis          | Secondary | Medium   | Adds a layer of business-relevant metrics, but not essential for core functionality. |
| Predictive Deviation Alerts | Future    | Low      | Requires a mature model and historical data; complex to implement.            |
| IoT + CRM Integration       | Future    | Low      | Expands data sources but adds complexity; MVP will focus on core ERP/MES data. |

### 1.2. Core Module Essentials

*   **Event Log Ingestion:** The system must be able to ingest data from CSV files. This is the simplest and most common format for exporting data from existing systems.
*   **Log Normalization:** The system must be able to map raw data columns (e.g., `Timestamp`, `Activity`, `Case ID`) to the required event log format.
*   **Process Discovery:** The system must implement a simple process discovery algorithm (e.g., a variant of the Alpha Miner) to generate a Petri net or a directly-follows graph.
*   **Conformance Checking:** The system must be able to perform token-based replay to identify deviations and calculate basic conformance metrics (e.g., fitness).
*   **Dashboard & Visualizer:** The dashboard must display the discovered process model and highlight deviations. It should be simple and focused on clarity.

---

## 2. System Architecture

A monolithic architecture is chosen for the MVP for simplicity of development and deployment. All services will be containerized for portability.

### 2.1. High-Level Architecture

```ascii
+--------------------------------------------------------------------------+
|                                  CEYEL MVP                               |
+--------------------------------------------------------------------------+
|                                                                          |
|   +-----------------+      +-----------------+      +-----------------+   |
|   |   Frontend      |----->|   API Layer     |----->|  Backend        |   |
|   |  (Dashboard)    |      |  (REST API)     |      |  (Services)     |   |
|   +-----------------+      +-----------------+      +-----------------+   |
|                                     |                      |             |
|                                     |                      |             |
|                                     v                      v             |
|                              +-----------------+      +-----------------+ |
|                              |   Database      |      |   Event Log     | |
|                              | (PostgreSQL)    |      |   Storage       | |
|                              +-----------------+      +-----------------+ |
|                                                                          |
+--------------------------------------------------------------------------+
```

### 2.2. Backend Services

```ascii
+--------------------------------------------------------------------------+
|                            Backend Services                              |
+--------------------------------------------------------------------------+
|                                                                          |
|   +-----------------+      +-----------------+      +-----------------+   |
|   | Event Ingestion |----->| Log Normalizer  |----->| Process Discovery|   |
|   | (CSV Parser)    |      | (Mapper)        |      | (Alpha Miner)   |   |
|   +-----------------+      +-----------------+      +-----------------+   |
|         |                                                |             |
|         |                                                v             |
|         |                                        +-----------------+   |
|         |                                        | Conformance     |   |
|         |                                        | Checker         |   |
|         |                                        +-----------------+   |
|         |                                                |             |
|         v                                                v             |
|   +------------------------------------------------------------------+   |
|   |                            Database                              |   |
|   +------------------------------------------------------------------+   |
|                                                                          |
+--------------------------------------------------------------------------+
```

### 2.3. Database Schema (Conceptual)

*   **`event_logs`**
    *   `log_id` (PK)
    *   `case_id`
    *   `activity_name`
    *   `timestamp`
    *   `resource` (optional)
    *   `raw_data` (JSONB)
*   **`process_models`**
    *   `model_id` (PK)
    *   `model_name`
    *   `model_data` (JSON/Graph format)
    *   `created_at`
*   **`conformance_results`**
    *   `result_id` (PK)
    *   `model_id` (FK)
    *   `case_id`
    *   `fitness_score`
    *   `deviations` (JSONB)

---

## 3. Data Flow

This section describes the end-to-end flow of data through the CEYEL system.

### 3.1. Data Ingestion to Model Generation

```
(START) --> [Upload CSV] --> [Event Ingestion Service] --> [Log Normalizer] --> [Database: event_logs] --> [Process Discovery Service] --> [Database: process_models] --> (END)
```

1.  **Upload CSV:** The user uploads a CSV file containing raw process data.
2.  **Event Ingestion Service:** The service parses the CSV file.
3.  **Log Normalizer:** The service maps the columns from the CSV to the standard event log format (`case_id`, `activity_name`, `timestamp`).
4.  **Database (event\_logs):** The normalized event logs are stored in the `event_logs` table.
5.  **Process Discovery Service:** The service queries the `event_logs` table and generates a process model.
6.  **Database (process\_models):** The generated process model is stored in the `process_models` table.

### 3.2. Conformance Checking and Dashboard Update

```
(START) --> [User Request: Conformance Check] --> [API Layer] --> [Conformance Checker] --> [Database: conformance_results] --> [API Layer] --> [Frontend Dashboard] --> (END)
```

1.  **User Request:** The user initiates a conformance check from the dashboard.
2.  **API Layer:** The request is routed to the Conformance Checker.
3.  **Conformance Checker:**
    *   Retrieves the process model from `process_models`.
    *   Retrieves the event logs from `event_logs`.
    *   Performs token replay.
    *   Calculates conformance metrics.
4.  **Database (conformance\_results):** The results are stored in the `conformance_results` table.
5.  **API Layer:** The frontend queries the API for the results.
6.  **Frontend Dashboard:** The dashboard visualizes the results, highlighting deviations on the process model.

---

## 4. Real-World Integration

This section outlines the practical steps for integrating CEYEL into a manufacturing environment.

### 4.1. Data Sources

The MVP will primarily target data from the following sources:

*   **Manufacturing Execution System (MES):** For production-related data.
*   **Enterprise Resource Planning (ERP):** For order and logistics data.
*   **Manual Logs:** For processes that are not yet digitized.

### 4.2. Ingestion Format

Data must be provided in CSV format with the following minimum columns:

*   `case_id`: A unique identifier for each process instance (e.g., `order_id`, `batch_id`).
*   `activity_name`: The name of the activity being performed (e.g., `Start Production`, `Quality Check`).
*   `timestamp`: The time the activity occurred, in `YYYY-MM-DD HH:MM:SS` format.

**Example CSV:**

```csv
case_id,activity_name,timestamp
101,Start Production,2025-12-01 08:00:00
101,Quality Check,2025-12-01 10:30:00
102,Start Production,2025-12-01 08:15:00
101,Package Item,2025-12-01 11:00:00
```

### 4.3. Integration Steps

1.  **Identify the Process:** Select a single, well-defined process to monitor (e.g., "order to cash," "production line A").
2.  **Extract Data:** Export the relevant data from the MES/ERP system into the specified CSV format.
3.  **Upload Data:** Upload the CSV file to the CEYEL platform.
4.  **Map Columns:** In the CEYEL UI, map the columns in the CSV file to the required fields (`case_id`, `activity_name`, `timestamp`).
5.  **Generate Model:** Initiate the process discovery to generate the initial process model.
6.  **Analyze Results:** Review the discovered model and conformance checking results on the dashboard.

---

## 5. Functional Specs

This section provides detailed specifications for each core module of the CEYEL MVP.

### 5.1. Event Ingestion

*   **Inputs:** A CSV file with a header row.
*   **Processing Logic:**
    *   Validate the file format (must be CSV).
    *   Parse the CSV and extract the header and data rows.
    *   Provide the header to the UI for column mapping.
*   **Outputs:** A JSON representation of the parsed CSV data.
*   **Constraints:** Maximum file size of 100MB for the MVP.

### 5.2. Log Normalizer

*   **Inputs:**
    *   The parsed CSV data (JSON).
    *   User-defined column mappings (e.g., `{"Case ID": "case_id", "Activity": "activity_name"}`).
*   **Processing Logic:**
    *   Iterate through each row of the data.
    *   Create a new event log entry for each row, using the mapped column names.
    *   Validate the data types (e.g., convert timestamp to a standard format).
*   **Outputs:** A list of normalized event log objects, ready to be stored in the database.
*   **Constraints:** Must handle missing values gracefully (e.g., by skipping the row and logging a warning).

### 5.3. Process Discovery

*   **Inputs:** A set of normalized event logs for a specific case.
*   **Processing Logic:**
    *   Implement a simple directly-follows graph algorithm.
    *   Identify the start and end activities.
    *   Calculate the frequency of each activity and the transitions between them.
*   **Outputs:** A graph-based representation of the process model (e.g., JSON format with nodes and edges).
*   **Constraints:** The algorithm should be able to handle simple parallel branches and loops.

### 5.4. Conformance Checker

*   **Inputs:**
    *   A process model.
    *   A set of event logs.
*   **Processing Logic:**
    *   Use token-based replay to compare the event logs against the process model.
    *   For each case, track the "tokens" as they move through the model.
    *   Identify missing tokens (activities that happened but were not expected) and remaining tokens (activities that were expected but did not happen).
*   **Outputs:**
    *   A fitness score (e.g., between 0 and 1).
    *   A list of deviations for each case.
*   **Constraints:** The checker must be able to handle incomplete traces.

---

## 6. Non-Functional Requirements

This section defines the quality attributes of the CEYEL MVP.

| Category          | Requirement                                                                                                 |
| ----------------- | ----------------------------------------------------------------------------------------------------------- |
| **Speed**         | Process discovery for a log of 10,000 events should complete in under 60 seconds.                           |
| **Reliability**   | The system should have an uptime of 99% during the pilot period.                                            |
| **Fault Tolerance** | If a service fails, it should be able to restart without data loss. Containerization will assist with this. |
| **Scalability**   | The system should be able to handle up to 1 million events in the database without significant performance degradation. |
| **Offline Capability** | Not required for the MVP. The system will be hosted on a local network.                                      |
| **Local Hosting** | The entire system must be deployable on-premise, within the factory's local network.                       |

---

## 7. Deployment Blueprint

This section provides instructions for deploying the CEYEL MVP.

### 7.1. Installation Steps

1.  Install Docker and Docker Compose.
2.  Clone the CEYEL repository.
3.  Create a `.env` file for configuration (database credentials, etc.).
4.  Run `docker-compose up -d` to build and start the services.
5.  Access the frontend at `http://localhost:3000`.

### 7.2. Dependencies

*   **Backend:** Python (FastAPI), Pandas, pm4py (for inspiration, not direct use)
*   **Frontend:** JavaScript (React, D3.js for visualization)
*   **Database:** PostgreSQL
*   **Infrastructure:** Docker

### 7.3. Containerization Plan

A `docker-compose.yml` file will define the following services:

*   `backend`: The Python application serving the REST API.
*   `frontend`: The React application serving the dashboard.
*   `db`: The PostgreSQL database.

### 7.4. Recommended Hardware (On-Premise)

*   **CPU:** 4 cores
*   **RAM:** 16 GB
*   **Storage:** 500 GB SSD

---

## 8. Testing Plan

This section outlines the testing strategy for the CEYEL MVP.

### 8.1. Unit Tests

*   Each service will have a suite of unit tests covering its core logic.
*   **Example:** A unit test for the Log Normalizer will check that it correctly maps columns.

### 8.2. Integration Tests

*   Integration tests will verify the interactions between services.
*   **Example:** An integration test will simulate a CSV upload and verify that the data is correctly stored in the database.

### 8.3. Sample Test Logs

A set of sample CSV files will be created to test various scenarios:

*   A "happy path" log with a simple, linear process.
*   A log with parallel branches.
*   A log with loops.
*   A log with missing data.

### 8.4. Pilot Testing in Factory

*   The MVP will be deployed in the Coimbatore manufacturing unit.
*   A specific production line will be selected for the pilot.
*   Data will be extracted from the MES and fed into CEYEL.
*   The results will be validated by the process owners.

### 8.5. Validation Metrics

*   **Conformance Fitness:** The calculated fitness score should match manual analysis.
*   **Model Accuracy:** The discovered process model should accurately reflect the real-world process.
*   **User Feedback:** The dashboard should be intuitive and provide actionable insights.

---

## 9. Deliverables Summary

This is a checklist of all the components that must be delivered for the CEYEL MVP.

- [ ] **Backend**
    - [ ] Event Ingestion Service (CSV)
    - [ ] Log Normalizer Service
    - [ ] Process Discovery Service (Directly-Follows Graph)
    - [ ] Conformance Checking Service (Token Replay)
    - [ ] REST API
- [ ] **Frontend**
    - [ ] Dashboard UI
    - [ ] Process Model Visualizer
    - [ ] CSV Upload Interface
- [ ] **Database**
    - [ ] PostgreSQL Schema
- [ ] **Deployment**
    - [ ] Docker Compose File
    - [ ] Installation Instructions
- [ ] **Testing**
    - [ ] Unit Tests
    - [ ] Integration Tests
    - [ ] Sample Test Logs
- [ ] **Documentation**
    - [ ] This MVP Blueprint
    - [ ] API Documentation (auto-generated)
