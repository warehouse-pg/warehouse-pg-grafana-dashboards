import os
import yaml
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv
import shutil
import json
import sys


# Load environment variables from .env.sample.sample file
load_dotenv()

try:
    WHPG_OBS_DSN_LIST=json.loads((os.getenv('WHPG_OBS_DSN_LIST',[])))
except json.JSONDecodeError:
    print("Error: WHPG_OBS_DSN_LIST environment variable contains invalid JSON.Make sure new line character is not present.")
    sys.exit(1)
if not WHPG_OBS_DSN_LIST:
    print("Error: WHPG_OBS_DSN_LIST is empty. Exiting.")
    sys.exit(1)

NUMBER_OF_WHPG_CLUSTER=int(os.getenv('NUMBER_OF_WHPG_CLUSTER', 1))
PROMETHEUS_RETENTION_TIME=os.getenv('PROMETHEUS_RETENTION_TIME', '90d')
PROMETHEUS_RETENTION_SIZE=os.getenv('PROMETHEUS_RETENTION_SIZE', '50GB')

# Store in the config
config = {
    'whpg_obs_dsn_list':WHPG_OBS_DSN_LIST,
    'prometheus_count': NUMBER_OF_WHPG_CLUSTER,
    'exporter_count': NUMBER_OF_WHPG_CLUSTER,
    'number_of_whpg_cluster': NUMBER_OF_WHPG_CLUSTER,
    'prometheus_retention_time': PROMETHEUS_RETENTION_TIME,
    'prometheus_retention_size': PROMETHEUS_RETENTION_SIZE
}

# Setup Jinja2 environment and load template
file_path = os.path.abspath(__file__)
file_dir = os.path.dirname(file_path)
project_dir = os.path.dirname(file_dir)

# Load template dir
env = Environment(loader=FileSystemLoader(os.path.join(file_dir,'templates')))
compose_template = env.get_template('docker-compose.yml.j2')

# Render template with config
rendered = compose_template.render(config=config)

# Create docker compose output
with open(os.path.join(project_dir,'docker-compose.yaml'), 'w') as f:
    f.write(rendered)
print("docker-compose.yml generated successfully.")

# Copy grafana-custom-dashboard.yaml
os.makedirs(os.path.join(project_dir, 'grafana', 'provisioning', 'dashboards'), exist_ok=True)
shutil.copy(os.path.join(file_dir,'grafana-custom-dashboard.yaml'), os.path.join(project_dir,'./grafana/provisioning/dashboards/'))
print("grafana-custom-dashboard.yaml copied successfully.")

# Render datasources.yaml
datasources_template = env.get_template('datasources.yaml.j2')
datasources_rendered = datasources_template.render(config=config)

os.makedirs(os.path.join(project_dir, 'grafana', 'provisioning', 'datasources'), exist_ok=True)
with open(os.path.join(project_dir,'./grafana/provisioning/datasources/datasources.yaml'), 'w') as f:
    f.write(datasources_rendered)
print("datasources.yaml generated successfully.")

# Generate prometheus config for each prometheus instance
os.makedirs(os.path.join(project_dir, 'prometheus'), exist_ok=True)
template = env.get_template('prometheus-instance.yaml.j2')
for i in range(1, NUMBER_OF_WHPG_CLUSTER + 1):
    rendered = template.render(instance_index=i)
    filename = os.path.join(project_dir, f'./prometheus/prometheus-{i:02d}.yaml')
    with open(filename, 'w') as f:
        f.write(rendered)
print("prometheus.yaml generated successfully.")

print(f"✅ Created docker compose for observability stack for {NUMBER_OF_WHPG_CLUSTER} cluster.")

