# Verwende ein Basis-Image, das Python enthält
FROM python:3.8-slim

# Installiere System-Abhängigkeiten
RUN apt-get update && \
    apt-get install -y \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Installiere die AWS CLI
RUN pip install awscli

# Installiere MLflow
RUN pip install mlflow

# Erstelle einen Ordner für MLflow-Daten
RUN mkdir -p /mlflow

# Kopiere das Start-Skript in den Container
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Setze Umgebungsvariablen für AWS-Anmeldeinformationen
ENV AWS_ACCESS_KEY_ID=AKIAZLJ6L32WQ5E3QWZJ
ENV AWS_SECRET_ACCESS_KEY=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

# Setze das Arbeitsverzeichnis
WORKDIR /mlflow

# Führe das Start-Skript aus
CMD ["/start.sh"]