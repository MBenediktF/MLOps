FROM python:3.9-slim

WORKDIR /app

COPY src/mlflow/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD ["sh", "-c", "mlflow ui --host 0.0.0.0 --port ${MLFLOW_PORT} --backend-store-uri ${MLFLOW_BACKEND_STORE_URI}"]