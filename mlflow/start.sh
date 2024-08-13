#!/bin/bash

# Synchronisiere Daten von S3 zum lokalen Verzeichnis
echo "Syncing MLflow data with S3..."
aws s3 sync s3://mlops-research/mlflow /mlflow --exact-timestamps

# Starte MLflow UI
echo "Starting MLflow UI..."
mlflow ui --host 0.0.0.0 --port 5000