# WarehousePG Observability docker composer

whpg_observability_docker_composer.py generates docker compose.yaml dynamically based on values mentioned in the .env file.
You can get an observability stack set up and running with Prometheus+Grafana for monitoring with few steps below - 
## Prerequisites
1. Install python 3.5 and above.(https://www.python.org/downloads/)
2. Install docker and docker compose plugin.(https://docs.docker.com/compose/install/)
3. Install git.

## Usage
In the main directory, type make to see a list of available options.

1. Create a .env file in the home directory by copying .env.sample and change the values for 
_NUMBER_OF_WHPG_CLUSTER_ which equates to number of whpg cluster want to monitor. Create a list for all the cluster
connection urls with the name _WHPG_OBS_DSN_LIST_.

2. Run below command to pull the latest exporter code, build docker image, pull docker images for prometheus and grafana
and lauch respective containers.
`make build`

3. Verify the containers
`make status`

4. Clean up the setup
`make clean`

## Start viewing dashboard in grafana
Log in Grafana (localhost:3000) with default username admin and password secret.(if not overrided in .env file) 

![Screenshot 2025-09-05 at 6.05.57 PM.png](Screenshot%202025-09-05%20at%206.05.57%E2%80%AFPM.png)

## FAQ