FROM python:3.10-slim

RUN mkdir -p /opt/dagster/dagster_home /opt/dagster/app

RUN pip install dagster-webserver dagster-postgres dagster-aws

# Copy your code and workspace to /opt/dagster/app
COPY src/dagster/repo.py src/dagster/workspace.yaml /opt/dagster/app/

ENV DAGSTER_HOME=/opt/dagster/dagster_home/

# Copy dagster instance YAML to $DAGSTER_HOME
COPY src/dagster/dagster.yaml /opt/dagster/dagster_home/

COPY src/dagster/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /opt/dagster/app

ENTRYPOINT ["sh", "-c", "dagster-webserver -h 0.0.0.0 -p $DAGSTER_PORT"]

