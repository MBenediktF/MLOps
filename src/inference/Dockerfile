FROM python:3.9-slim

WORKDIR /app

COPY src/inference/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/inference/. ./

ENV FLASK_APP=flask_app.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

CMD ["flask", "run"]
