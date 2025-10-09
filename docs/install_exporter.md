# Setting Up the WarehousePG Observability Exporter
The **Observability Exporter** queries the views in the observability schema and exposes WarehousePG metrics at the _/metrics_ endpoint.
These metrics can be scraped by **Prometheus** and visualized in **Grafana**.

The exporter can be installed either on the coordinator host or on any other Linux host.

## Steps to install and configure the exporter
1. Set up the EDB repository
    1. To determine if your repository exists, enter this command:
        ```
        dnf repolist | grep enterprisedb
        ```
        If no output is generated, the repository isn't installed.
   2. Go to EDB [repositories](https://www.enterprisedb.com/repos-downloads).
   3. Select the button that provides access to the EDB repository.
   4. Select the platform and software that you want to download.
   5. Follow the instructions for setting up the EDB repository.
2. Install the exporter RPM
    ```
    sudo dnf install edb-whpg7-observability-exporter.rpm
    ```
   
3. Configure the connection URL<br >
     Set the environment variable to allow the exporter to connect to the WarehousePG cluster:
   ```
    export WHPG_OBS_DSN="host=<host> port=<port> dbname=<db_name> user=<user> password=<password> sslmode=disable"
    ```

4. (Optional) Customize exporter settings<br>
You can adjust the port and log level using environment variables:
    ```
    export WHPG_OBS_PROM_PORT=<port_number>     # Default: 9187
    export WHPG_OBS_LOG_LEVEL=<level>           # Options: debug, info, warn
   ```

5. Start the exporter
    ```
   whpg_observability_exporter &1>&2 &2>logfile.txt &
   ```
   This will start and run exporter process in the background.

6. Verify the exporter<br>
   Access the metrics endpoint in the browser to confirm the exporter is running:
    ```
   http://localhost:<WHPG_OBS_PROM_PORT:-9187>/metrics
   ```
    You should see a list of metrics that can be consumed by Prometheus and visualized in Grafana.
    




