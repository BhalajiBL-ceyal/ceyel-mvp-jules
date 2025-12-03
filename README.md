# CEYEL MVP

This is the Minimum Viable Product for the CEYEL Process Mining platform. It provides a complete, containerized application for ingesting event logs, discovering process models, and performing conformance checking.

## Prerequisites

- Docker
- Docker Compose

## How to Run

1.  **Clone the repository:**
    ```sh
    git clone <repository-url>
    cd ceyel-mvp
    ```

2.  **Build and start the services:**
    ```sh
    docker-compose up --build
    ```
    This command will build the Docker images for the backend and frontend, start the containers, and initialize the database.

3.  **Access the application:**
    -   The **frontend** will be available at [http://localhost:3000](http://localhost:3000).
    -   The **backend API** will be available at [http://localhost:8000](http://localhost:8000).

## How to Use

1.  **Open the frontend** in your browser at [http://localhost:3000](http://localhost:3000).
2.  **Upload a CSV file** containing an event log. A sample file (`sample_log.csv`) is provided in the `database` directory.
    -   The CSV must have the following columns: `case_id`, `activity_name`, `timestamp`.
3.  Click the **"Discover Process"** button.
4.  The application will automatically:
    -   Ingest the event log.
    -   Discover a Directly-Follows Graph (DFG) process model.
    -   Render the process model on the screen.

## Project Structure

-   `/backend`: Contains the Python FastAPI application.
-   `/frontend`: Contains the React/TypeScript application.
-   `/database`: Contains the database initialization script and sample data.
-   `docker-compose.yaml`: Orchestrates all the services.

## Developer Notes

-   To run the backend tests (once implemented), you would typically run `pytest` inside the backend container.
-   The frontend is built with `create-react-app` and can be developed locally by running `npm start` in the `frontend` directory. You would need to configure a proxy in `package.json` to forward API requests to the backend.
-   The database schema is defined in `database/init.sql`. Any changes to the schema should be made there.
