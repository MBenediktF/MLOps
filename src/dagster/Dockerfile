FROM python:3.10-slim

RUN mkdir -p /opt/dagster/dagster_home /opt/dagster/app

# System dependency libgl1 & libglib2 for opencv
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install requirements
COPY src/dagster/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy code and workspace to /opt/dagster/app
# 1: Dasgter Files
COPY src/dagster/workspace.yaml /opt/dagster/app/
COPY src/dagster/definitions.py /opt/dagster/app/
COPY src/dagster/assets/. /opt/dagster/app/assets/
COPY src/dagster/jobs/. /opt/dagster/app/jobs/
COPY src/dagster/sensors/. /opt/dagster/app/sensors/
COPY src/dagster/schedules/. /opt/dagster/app/schedules/
# 2: Helpers
COPY src/helpers/. /opt/dagster/app/helpers/
# 3: MySQL Tables
COPY src/model/tables/. /opt/dagster/app/tables/
# 4: Model Scripts
COPY src/model/create_dataset.py /opt/dagster/app/
COPY src/model/components/. /opt/dagster/app/model/

# Directory structure
# /opt/dagster/
# └── app/
#     ├── workspace.yaml           # Dagster workspace configuration
#     ├── definitions.py           # Dagster pipeline definitions
#     ├── assets/                  # Asset files for Dagster
#     │   └── ...                  
#     ├── jobs/                    # Job files for Dagster
#     │   └── ...               
#     ├── schedules/               # Schedule files for Dagster
#     │   └── ...                     
#     ├── sensors/                 # Sensor files for Dagster
#     │   └── ...                  
#     ├── helpers/                 # Helper files
#     │   └── ...                  
#     ├── tables/                  # MySQL Table definitions
#     │   └── ...                  
#     ├── model/                   # Model scripts
#     │   └── ...          
#     └── create_dataset.py        # Python script to create datasets

ENV DAGSTER_HOME=/opt/dagster/dagster_home/

# Copy dagster instance YAML to $DAGSTER_HOME
COPY src/dagster/dagster.yaml /opt/dagster/dagster_home/

WORKDIR /opt/dagster/app

ENTRYPOINT ["sh", "-c", "dagster-webserver -h 0.0.0.0 -p $DAGSTER_PORT"]
