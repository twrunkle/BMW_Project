# To build the database container, use this command.

docker build -t telemetry-db:latest .
docker run -d \
  --name telemetry-db \
  -p 5432:5432 \
--restart=always \
  telemetry-db:latest
