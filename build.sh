#!/bin/bash
set -e

# This script builds the Go binary and creates an RPM using a CentOS 7 Docker container.
# Usage: ./build.sh


# Variables
PARENT_DIR=$(dirname "$PWD")
PROJECT_DIR_NAME=$(basename "$PWD")

# 1.Clone and create a docker image for exporter
echo "Cloning/Updating & building Docker image for WHPG-exporter (amd64 platform)..."
if [ -d "warehouse-pg-observability-exporter/.git" ]; then
  echo "Updating existing repo..."
  cd exporter && git pull
else
  echo "Cloning repo..."
  git clone https://github.com/warehouse-pg/warehouse-pg-observability-exporter.git
fi

cd ./warehouse-pg-observability-exporter
docker build --platform=linux/amd64 -t whpg_exporter -f ./Dockerfile .


# 2. Create docker image to create docker compose
echo "Building Docker image for docker compose build (amd64 platform)..."
cd "$PARENT_DIR"/"$PROJECT_DIR_NAME"
docker build --platform=linux/amd64 -t compose-builder -f ./Dockerfile .

# 4. Create dirs -
mkdir -p ./grafana/provisioning/datasources
mkdir -p ./grafana/provisioning/dashboards
mkdir -p ./prometheus

# 3. Build docker compose
docker run --platform=linux/amd64 --rm \
    -v $PWD:/app \
    compose-builder bash -c "\
        source /home/Venv/bin/activate
        pip install -r /app/compose_creator/requirements.txt
        python3 /app/compose_creator/whpg_observability_docker_composer.py
    "
echo "docker compose creation is complete. Check the project folder for docker-compose.yaml"

echo "Performing cleanup..."
# Cleanup Docker image
docker rmi -f compose-builder > /dev/null 2>&1 || true
echo "Docker image compose-builder removed."
