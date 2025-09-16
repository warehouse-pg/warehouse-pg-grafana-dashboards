# WHPG cluster info (Mandatory)
NUMBER_OF_WHPG_CLUSTER=2
WHPG_OBS_DSN_DICT= {
    "Prod": "host=host.docker.internal port=6432 dbname=whpgtest user=gpadmin password=postgres sslmode=disable",
    "Test": "host=host.docker.internal port=6431 dbname=whpgtest user=gpadmin password=postgres sslmode=disable"
}


# WHPG  exporter setting. (Optional)
WHPG_OBS_LOG_LEVEL='debug'

# Prometheus settings. (Optional)
PROMETHEUS_RETENTION_TIME='90d'
PROMETHEUS_RETENTION_SIZE='50GB'

# Grafana settings. (Optional)
GRAFANA_ADMIN_USER='admin'
GRAFANA_PASSWORD='secret'
GRAFANA_PORT=3000
