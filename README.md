# Grafana Dashboards for WarehousePG

## Observability for WarehousePG

The Observability for [WarehousePG](https://warehouse-pg.io/) (WHPG) consists of two separate packages: This is intentional in order to separate the data gathering from data storage and data display. This approach allows to minimize required permissions to the database, and also allows multiple forms of visualization and alerting.

* Data gathering: the WarehousePG Observability Extension (part 1)
* Data exporting: the WarehousePG Observability Exporter (part 2)
* Data storage: Prometheus for historical data storage (example implementation)
* Data visualization: the WarehousePG Grafana dashboard (example dashboards)

## WarehousePG Observability Extension

The *WarehousePG Observability Extension* is a database extension and is installed using `CREATE EXTENSION` in the WarehousePG database. Currently versions 6 and 7 of WarehousePG are supported.

EDB provides the extension as RPM package for various RHEL versions and compatible platforms.

The database extension creates the `observability` schema in the database, which includes a number of views and external tables. A superuser account is required in order to access views in this schema.

### Installation of the extension

Download the RPM from the EDB repository, and install it on all hosts (coordinator, standby, and all segments).

RHEL 7:

```
sudo dnf install edb-whpg7-observability
```

RHEL 6:

```
sudo yum install edb-whpg7-observability
```

In a database of your choice, execute the following command:

```
CREATE EXTENSION whpg_observability;
```

We recommend that you create a separate database for observability, and limit access to the account used for the Prometheus Exporter (see later steps in this document) to this database.

Configure access for the Prometheus Exporter account in `pg_hba.conf`, see the [documentation](https://warehouse-pg.io/docs/7x/admin_guide/getting_started.html) about configuring roles and access.

### Available views

The views are documented in the [Extension documentation](Extension.md).

## WarehousePG Observability Exporter

The [Prometheus Exporter](https://prometheus.io/docs/instrumenting/exporters/) connects to the WHPG database and exclusively uses the views in the `observability` schema to gather data. This data is exported in machine-readable format to be consumed by Grafana and other tools.

The Exporter must be able to connect to the WHPG database, and requires a superuser account. The Exporter is lightweight and does not require a lot of CPU or memory resources. It can run on the coordinator, the standby, or an external host.

To install the observability exporter, follow the instructions here.

### Steps to install and configure the exporter

1. Download and install the exporter RPM from EDB repository.

RHEL 7:

```
sudo dnf install edb-whpg7-observability-exporter
```

RHEL 6:

```
sudo yum install edb-whpg7-observability-exporter
```
   
2. Configure the connection URL

Set the environment variable to allow the exporter to connect to the WarehousePG cluster:

```
export WHPG_OBS_DSN="host=<host> port=<port> dbname=<db_name> user=<user> password=<password> sslmode=disable"
```

3. (Optional) Customize exporter settings

You can adjust the port and log level using environment variables:

```
export WHPG_OBS_PROM_PORT=<port_number>     # Default: 9187
export WHPG_OBS_LOG_LEVEL=<level>           # Options: debug, info, warn
```

Note: the default port for the Prometheus dataabse is `9187`.

4. Start the exporter

```
whpg_observability_exporter 1>logfile.txt 2>&1 &
```

This will start and run the exporter process in the background.

Note: You can either start the process when the system reboots or include it in your startup init script.

5. Verify the exporter

Access the metrics endpoint in the browser to confirm the exporter is running:

```
http://localhost:<WHPG_OBS_PROM_PORT:-9187>/metrics
```

You should see a list of metrics that can be consumed by Prometheus and visualized in Grafana.

## Configuring Prometheus

Add the exporter to the scrape_configs section of your prometheus.yml configuration file:

```
   - job_name: whpg_cluster_monitoring
      scrape_interval: 30s
      scrape_timeout: 28s
      static_configs:
        - targets:
          - "<exporter_url>:<exporter_port>"
```

**scrape_interval** and **scrape_timeout** should be configured based on the WarehousePG cluster's response time.

Generally, scrape_timeout should be slightly less than scrape_interval.

To determine an appropriate scrape_interval, use the following command to measure the current response time:

```
curl -w "Total time: %{time_total} seconds\n" -o /dev/null -s <exporter_url>:<exporter_port>/metrics
```

## Configuring Grafana

[Grafana](https://grafana.com/) is a visualization tool for data gathered by other tools (as example [Prometheus Exporter](https://prometheus.io/docs/visualization/grafana/)) or by directly querying data sources.

While Grafana can directly connect to the WHPG database and use the views provided by the `observability` schema, we strongly recommend separating the access between Grafana and WHPG by exporting the data using the Prometheus Exporter. This has the additional advantage that the Exporter continuously exports and stores the data, and provides historical data.

EDB provides a set of JSON configuration files for Grafana in the [Grafana Dashboards for WarehousePG](https://github.com/warehouse-pg/warehouse-pg-grafana-dashboards/example-dashboards/) repository. We understand that users have different needs for monitoring. The provided Grafana configurations provide a starting point for customization.

### Configuring Data Source and Importing Dashboards into Grafana

1. Add Prometheus as a data source:

* Log in to Grafana with Admin privileges.
* Go to Connections > Data Sources.
* Click Add new data source.
* Select Prometheus.
* Enter the Prometheus server URL (e.g., http://<prometheus_host>:9090).
* Click Save & Test.

2. Import WarehousePG Dashboard:

* Download WarehousePG dashboard JSON file here.
* In Grafana, go to Dashboards.
* Click on the New dropdown and select Import.
* Upload the JSON file or paste its content.
* Click Import.
* Repeat the same step for importing the WarehousePG Detailed View dashboard.

3. Access Dashboard

Navigate to Dashboards in Grafana and select the WarehousePG dashboard to view the monitoring graphs.
