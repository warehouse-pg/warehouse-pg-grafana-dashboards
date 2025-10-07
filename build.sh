#!/bin/bash
set -e

# This script builds the Go binary and creates an RPM using a CentOS 7 Docker container.
# Usage: ./build.sh

# Variables
PARENT_DIR=$(dirname "$PWD")
PROJECT_DIR_NAME=$(basename "$PWD")

# 1.Switch to project dir
cd "$PARENT_DIR"/"$PROJECT_DIR_NAME"

# 2.Create linux container image which has exporter rpm installed
echo "Building Docker image for exporter container (amd64 platform)..."
docker build --secret id=edbtoken_secret,src=$HOME/.edb-token --secret id=edbrepository_secret,src=$HOME/.edb-repository --platform=linux/amd64 -t whpg_exporter -f ./compose_creator/DockerfileExporter .

# 3. Create docker image to create docker compose
echo "Building Docker image for docker compose generation (amd64 platform)..."
docker build --platform=linux/amd64 -t compose-builder -f ./compose_creator/DockerfileComposeCreation .

# 4. Create dirs -
echo "Creating directories..."
mkdir -p ./grafana/provisioning/datasources
mkdir -p ./grafana/provisioning/dashboards
mkdir -p ./prometheus

# 5. Create docker compose
echo "Generating docker compose..."
docker run --platform=linux/amd64 --rm \
    -v $PWD:/app \
    compose-builder bash -c "\
        source /home/Venv/bin/activate
        pip install -r /app/compose_creator/requirements.txt
        python3 /app/compose_creator/whpg_observability_docker_composer.py"

echo "Performing cleanup..."
# Cleanup Docker image
docker rmi -f compose-builder > /dev/null 2>&1 || true
echo "Docker image compose-builder removed."
echo "✅ Docker compose generation is complete. Check the project folder for docker-compose.yaml"
