# WarehousePG Observability Docker Setup

This repository provides a way to create Docker configurations for setting up WarehousePG cluster observability 
for multiple clusters using WHPG Exporter, Prometheus, and  Grafana.

## Prerequisites
1. Install Docker and Docker Compose plugin.(https://docs.docker.com/compose/install/)
2. Install `git` and `make` tools.
3. Make sure you have the extension installed on all the WarehousePG clusters.(https://github.com/warehouse-pg/warehouse-pg-observability-extension)

## EDB Token

You need an EDB token in order to download RPM packages:

To get a token:

- go to `https://enterprisedb.com/`
- Sign in
- Go to "My Account" (in the upper right corner)
- Select "Account Settings" from Dropdown
- Under "Profile", copy the first line, that's the "Repos 2.0" token
- Create the file "~/.edb-token" and copy the token into the file

Your token matches a specific repository. You should have received this information along with the token.
For EDB employees the personal token is for the "dev" repository.
Create the file "~/.edb-repository", add one of: "dev", "staging_gpsupp", "gpsupp".


## Usage
In the main directory, type make to see a list of available options.

### Configuring cluster details to monitor
Create a _config_local.py_ file in the home directory by copying _config.py_ and change the values for 
_NUMBER_OF_WHPG_CLUSTER_ which equates to the number of WarehousePG clusters to monitor. 
Create a dictionary which contains key pairs with _cluster_name:cluster_connection_url_

### make build
Will build a Docker image which has exporter rpm installed, pull Docker images for Prometheus and Grafana.
`make build`

### make run
Will launch all the containers
`make run`

### make status
Shows the running Docker containers.

### make stop
Stops the containers.

### make clean
Cleans everything

## Start viewing dashboard in Grafana
Log in Grafana (localhost:3000) with default username admin and password secret (if not overridden in .env file) 
![dashboard.png](dashboard.png)

## FAQ
