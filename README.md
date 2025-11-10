# WHPG Grafana & Prometheus Monitoring Setup

> [!CAUTION]
> This feature is in Technical Preview and not yet recommended for production deployments. We recommend that you try this feature in test or development environments.

This repository provides a **ready-to-run monitoring stack** for WarehousePG using **Prometheus** and **Grafana**. It includes pre-configured dashboards, data sources, and support for custom exporters. This setup runs an independent Prometheus and Grafana stack using Docker Compose.

It is designed to be a central monitoring point, capable of scraping metrics from:

* Other Docker containers running on the same host (e.g., exporters from another compose stack).
* Remote servers (e.g., EC2 instances on AWS).


---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Setup Instructions](#setup-instructions)
4. [Configuring a New Exporter](#configuring-a-new-exporter)
5. [The Checklist](#the-checklist)
6. [Common Docker Commands](#common-docker-commands)

---

## Overview

This stack consists of:

| Service           | Image / Version        | Purpose                                     |
| ----------------- | ---------------------- | --------------------------------------------|
| `prometheus-whpg` | prom/prometheus:v3.5.0 | Collects metrics from WarehousePG exporters. Accessible at http://localhost:9092 |
| `grafana-whpg`    | grafana/grafana:12.1.1 | Visualization and dashboards. Accessible at http://localhost:3001 (User: admin, Pass: secret)                |

Prometheus scrapes metrics from one or more `whpg_exporter` instances. Grafana reads data from Prometheus and displays it on  pre-configured dashboards.

---

## Prerequisites

* Docker Desktop (Mac/Windows) or Docker Engine (Linux)
* Network connectivity between Docker containers and exporter targets.

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

   * URL: `http://localhost:3001`
   * Default credentials:

     * User: `admin`
     * Password: `secret`

4. **Prometheus** is accessible at `http://localhost:9092`.

---

## Configuring a new Exporter



**Update Prometheus configuration** (`prometheus/prometheus.yaml`) to configure a new exporter. After any change to prometheus.yaml, you must restart Prometheus:
 ```
 docker-compose up -d --force-recreate prometheus-whpg
```

***Case 1: Scraping Local Docker Exporters (Same Host, Different Compose)***
   ```yaml
   scrape_configs:
     - job_name: 'whpg_exporter'
       static_configs:
       # Use host.docker.internal and the HOST port (9187)
         - targets: ['host.docker.internal:9187']
   ```
* Use host.docker.internal to allow the Prometheus container to access the host's ports.
* Port 9187 must match the container port the exporter exposes.
* On Linux, Docker containers cannot automatically resolve host.docker.internal. To scrape exporters running on the same Linux host, add this to docker-compose.yml under the Prometheus service:

   ```
    extra_hosts:
      - "host.docker.internal:host-gateway"
  ```
***Case 2: Scraping a Remote Exporter (e.g., on AWS)***

Use the server's public IP address and the exposed port. Ensure the firewall or Security Group allows inbound traffic from the Prometheus host/container.Then, **restart Prometheus** to pick up the changes:

   ```
     scrape_configs:
     - job_name: 'remote-aws-node'
       static_configs:
        # Use the PUBLIC IP of the AWS server and its exporter port
        - targets: ['54.12.34.56:9187']
   ```
---

## The Checklist

For the entire system to work, these four connections must be correct.

1. **Prometheus <-> Exporter (Network)** 

Prometheus must be able to reach the exporter IP/host and port. On AWS, ensure Security Groups allow access; on Linux, extra_hosts may be required for host services

2. **Prometheus <-> Config (Scraping)** 

The targets list in prometheus.yaml must match the exact container/service names, hostnames, or IPs and ports of exporters. This is how Prometheus finds the metrics endpoints.

3. **Grafana <-> Prometheus (Datasource URL)** 

The url in grafana/datasources/datasource.yaml must match the service: name in docker-compose.yaml (prometheus-whpg) and its internal port (9090). This is how Grafana finds the Prometheus server.

4. **Grafana <-> Dashboard (Datasource UID)** 

The UID in grafana/datasources/datasource.yaml must match the datasource UID referenced in dashboards. This ensures dashboards load with the correct datasource automatically.

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
   docker-compose restart prometheus-whpg
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
   docker-compose logs -f grafana-whpg
   ```

