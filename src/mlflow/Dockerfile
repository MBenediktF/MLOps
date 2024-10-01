FROM python:3.9-slim

WORKDIR /app

COPY src/mlflow/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD ["mlflow", "ui", "--host", "0.0.0.0", "--port", "5003"]
