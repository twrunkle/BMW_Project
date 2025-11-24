#To build and run backend container, run this command on CLI.

docker build -t backend_web:latest .
docker run -d \
  --name backend_web \
  -p 8000:8000 \
  -e DB_HOST=172.31.23.88 \
  -e DB_NAME=telemetry_data \
  -e DB_USER=telemetry_backend \
  -e DB_PASS=password \
--restart=always \
  backend_web:latest
