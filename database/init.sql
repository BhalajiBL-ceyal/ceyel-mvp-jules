-- CEYEL MVP Database Schema
-- Version: 1.0

-- Best practice: Run these commands inside a transaction
BEGIN;

-- Table for storing individual events
CREATE TABLE IF NOT EXISTS event_logs (
    event_id SERIAL PRIMARY KEY,
    case_id VARCHAR(255) NOT NULL,
    activity_name VARCHAR(255) NOT NULL,
    event_time TIMESTAMPTZ NOT NULL,
    details JSONB, -- For storing any extra data associated with the event
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for efficient querying by case_id
CREATE INDEX IF NOT EXISTS idx_event_logs_case_id ON event_logs (case_id);

-- Table for storing discovered process models
CREATE TABLE IF NOT EXISTS process_models (
    model_id SERIAL PRIMARY KEY,
    model_name VARCHAR(255) NOT NULL,
    model_data JSONB NOT NULL, -- Storing the graph (nodes and edges)
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Table for storing the results of conformance checks
CREATE TABLE IF NOT EXISTS conformance_results (
    result_id SERIAL PRIMARY KEY,
    model_id INTEGER REFERENCES process_models(model_id),
    fitness_score REAL NOT NULL,
    deviations JSONB, -- Storing a list of deviation objects
    checked_at TIMESTAMPTZ DEFAULT NOW()
);

COMMIT;
