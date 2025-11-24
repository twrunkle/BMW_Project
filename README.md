# Setup Database on a New Instance

1. Make sure Docker and Docker Compose are installed:
# Update package index
sudo apt update

# Install prerequisites
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update again and install Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Start Docker and enable on boot
sudo systemctl start docker
sudo systemctl enable docker

# Verify installation
docker --version

3. Clone the repository:
   git clone repo-url
4. Change into the repo directory:
   cd repo-name
5. Start the containers:
   docker-compose up -d
6. Verify the database:
   docker exec -it telemetry_db psql -U telemetry_backend -d telemetry_data
   \dt   # list tables
7. If needed, run any SQL scripts necessary
