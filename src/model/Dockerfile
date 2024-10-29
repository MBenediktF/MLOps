FROM python:3.9-slim

WORKDIR /app

# System dependency libgl1 & libglib2 for opencv
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY src/model/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/model/. ./
COPY src/helpers/. ./helpers/

ENV FLASK_APP=flask_app.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["sh", "-c", "flask run --port ${MODEL_TRAINING_PORT}"]