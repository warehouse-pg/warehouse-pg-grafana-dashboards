# WarehousePG Observability Docker Setup

This repository provides a way to create Docker configurations for setting up WarehousePG cluster observability 
for multiple clusters using WHPG Exporter, Prometheus, and  Grafana.

## Prerequisites
1. Install Docker and Docker Compose plugin.(https://docs.docker.com/compose/install/)
2. Install git.
3. Make sure you have the extension installed on all the WarehousePG clusters.(https://github.com/warehouse-pg/warehouse-pg-observability-extension)

## Usage
In the main directory, type make to see a list of available options.

1. Create a _config_local.py_ file in the home directory by copying _config.py_ and change the values for 
_NUMBER_OF_WHPG_CLUSTER_ which equates to the number of WarehousePG clusters to monitor. 
Create a dictionary which contains key pairs with _cluster_name:cluster_connection_url_

2. Run the command below to pull the latest exporter code, build a Docker image, pull Docker images for Prometheus and Grafana, and launch respective containers.
`make build`

3. Launch all the containers with
`make run`

5. Verify the containers
`make status`

6. Stop the containers.
`make stop`

7. Clean everything
`make clean`

## Start viewing dashboard in Grafana
Log in Grafana (localhost:3000) with default username admin and password secret (if not overridden in .env file) 
![dashboard.png](dashboard.png)

## FAQ
