# Use official Python image
FROM python:3.11-slim

WORKDIR /home
# Create Python virtual environment
RUN python -m venv Venv

# Activate the virtual environment and install requirements (optional)
# If you have requirements.txt, uncomment next lines:
RUN . Venv/bin/activate
RUN pip install --upgrade pip
# RUN ls -la
# RUN pip install -r /app/compose_creator/requirements.txt
# RUN python3 /app/compose_creator/whpg_observability_docker_composer.py

# Set default command to bash so you can enter container shell
CMD ["bash"]
