import os
import yaml
from jinja2 import Environment, FileSystemLoader
import shutil
import sys
import importlib.util


# Setup dirs variables
file_path = os.path.abspath(__file__)
file_dir = os.path.dirname(file_path)
project_dir = os.path.dirname(file_dir)

# Add path to config directory
CONFIG_PATH = os.path.abspath(os.path.join(project_dir,'config.py'))
sys.path.insert(0, project_dir)

# import config
import config

# Path to config_local.py
local_config_path = os.path.join(project_dir, "config_local.py")

if os.path.exists(local_config_path):
    spec = importlib.util.spec_from_file_location("config_local", local_config_path)
    config_local = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config_local)

    # Override attributes in config with those from config_local
    for attr in dir(config_local):
        if not attr.startswith("__"):
            setattr(config, attr, getattr(config_local, attr))

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
for cluster, cluster_dsn in config.WHPG_OBS_DSN_DICT.items():
    rendered = template.render(cluster=cluster)
    filename = os.path.join(project_dir, f'./prometheus/prometheus-{cluster:02s}.yaml')
    with open(filename, 'w') as f:
        f.write(rendered)
print("prometheus.yaml generated successfully.")

print(f"Created docker compose for observability stack for {config.NUMBER_OF_WHPG_CLUSTER} cluster.")

