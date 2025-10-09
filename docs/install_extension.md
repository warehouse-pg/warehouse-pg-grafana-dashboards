# Installing the Observability Extension

To install the observability extension, follow the instructions here.

You need to install this extension on the **coordinator**, **standby**, and **all segment hosts**.

## Steps to install the extension
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

2. Download the extension on the coordinator
    ```
    sudo dnf download edb-whpg7-observability.x86_64
   ```
3. Copy the RPM to all hosts<br/>Ensure that the all_hosts file contains the list of hostnames for all nodes in the cluster.
    ```
    gpscp -f /home/gpadmin/all_hosts /tmp/edb-whpg7-observability.x86_64.rpm /tmp/
    ```
4. Install the extension RPM
   ```
   gpssh -f /home/gpadmin/all_hosts "cd /tmp; sudo dnf install -y --disablerepo=* /tmp/whpg_observability*.rpm"
   ```
5. Create the extension in the database<br/>Connect to the coordinator using psql and run:
    ```
   CREATE EXTENSION IF NOT EXISTS whpg_observability;
   ```
   This command creates the observability schema, which provides views for querying cluster observability data.
