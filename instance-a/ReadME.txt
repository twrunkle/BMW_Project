To build and run frontend container, run this command on CLI.

docker build -t collector_web:latest ~/collector
docker run -d \
  --name collector_web \
  -p 9000:9000 \
  -v /home/ubuntu/collector/data:/app/data \
  -v /home/ubuntu/collector/app/templates:/app/templates \
  --restart=always \
  collector_web:latest
