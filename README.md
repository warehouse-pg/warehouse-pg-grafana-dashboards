# WHPG Monitoring Setup

This repository provides a **ready-to-run monitoring stack** for WarehousePG using **Prometheus**, **Loki** and **Grafana**. It includes pre-configured dashboards, data sources, and support for custom exporters. This setup runs an independent Prometheus, Loki and Grafana stack using Docker Compose.

`NOTE` 
 -This monitoring stack only visualizes data; it does not collect it. To see operational data on the dashboards, user must first install and configure the separate WarehousePG Observability Suite (including the Extension, Collector, and Exporter components) to ensure metrics and logs are correctly shipped to the Prometheus and Loki services within this environment.

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Setup Instructions](#setup-instructions)
4. [The Checklist](#the-checklist)
5. [Common Docker Commands](#common-docker-commands)

---

## Overview

This stack consists of:

| Service           | Image / Version        | Purpose                                     |
| ----------------- | ---------------------- | --------------------------------------------|
| `prometheus` | prom/prometheus:v3.5.0 | Receives data from WarehousePG Exporter, Collector and Loki. Accessible at http://localhost:9090 |
| `loki` | grafana/loki:3.5 | Receives metrics from WarehousePG Collector.|
| `grafana`    | grafana/grafana:12.3 | Visualization and dashboards. Accessible at http://localhost:3000 (User: admin, Pass: admin)                |



---

## Prerequisites

* Docker Desktop (Mac/Windows) or Docker Engine (Linux)
* Network connectivity

---

## Setup Instructions

1. **Clone the repository**

   ```
   git clone <repo-url>
   cd warehouse-pg-grafana-dashboards
   ```

2. **Start the monitoring stack**

   ```
   docker-compose up -d
   ```

3. **Access Grafana**

   * URL: `http://localhost:3000`
   * Default credentials:

     * User: `admin`
     * Password: `admin`

4. **Prometheus** is accessible at `http://localhost:9090`.

---


## The Checklist

For the entire system to work, following connections must be correct.

1. **Grafana <-> Prometheus (Datasource URL)** 

The url in grafana/datasources/datasource.yaml must match the service: name in docker-compose.yaml (prometheus) and its internal port (9090). This is how Grafana finds the Prometheus server.

2. **Grafana <-> Loki (Datasource URL)** 

The url for Loki in grafana/datasources/datasource.yaml must match the Loki service: name in docker-compose.yaml (Loki) and its internal port (3100). This is how Grafana finds the Loki server.

3. **Grafana <-> Exporter (Datasource URL)** 

The Exporter extends an endpoint to Grafana, using which the user can get predefined live metrics from the database. This url is defined in the grafana/datasources/datasource.yaml , and  is of the form  `http://<exporter-ip>:9187/api/v1/query`.

4. Remote write should be enabled on the Prometheus, it is done by including `--web.enable-remote-write-receiver` while defining Prometheus service in the docker compose. 

## Common Docker Commands

1. Start the stack (in background):

   ```
   docker-compose up -d
   ```

2. Stop the stack

   ```
   docker-compose down
   ```

3. Restart a single service: (e.g., to apply changes to prometheus.yaml)

   ```
   docker-compose restart prometheus
   ```

4. View all running containers:

   ```
   docker ps
   ```

5. Check which containers are on network

   ```
   docker network inspect <network-name>
   ```

5. View live logs for one service: (Press Ctrl+C to exit)

   ```
   docker-compose logs -f grafana
   docker-compose logs -f prometheus
   docker-compose logs -f loki
   ```

