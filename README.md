# Setup Database on a New Instance

#1. Make sure Docker and Docker Compose are installed.
#2. Clone the repository:
#   git clone <repo-url>
#3. Change into the repo directory:
#   cd <repo-name>
#4. Start the containers:
#   docker-compose up -d
#5. Verify the database:
#   docker exec -it telemetry_db psql -U telemetry_backend -d telemetry_data
#   \dt   # list tables
#6. If needed, run any SQL scripts necessary
