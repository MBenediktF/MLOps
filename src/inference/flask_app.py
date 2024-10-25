from inference_pipeline import InferencePipeline  # noqa: F401
from flask import Flask, request, jsonify, send_file
import shutil
import os

SECRET_TOKEN = ""

app = Flask(__name__)

model_name = "Dev-Live"
model_version = "1"
measurement = "m2"
inference_pipeline = InferencePipeline(model_name, model_version, measurement)


@app.route("/")
def index():
    return """
        <h1>Inference API is running</h1>
        <ul>
            <li><a href="/show_logs">Show Logs</a></li>
            <li><a href="/show_data_logs">Show Data Logs</a></li>
            <br>
            <li><a href="/get_logs">Download Logs</a></li>
            <li><a href="/get_data_logs">Download Data Logs</a></li>
        </ul>
    """


@app.route("/show_logs")
def show_logs():
    try:
        shutil.copy("logs/inference_pipeline.log", "inference_pipeline.log")
        response = send_file(
            "inference_pipeline.log",
            mimetype="text/plain",
            as_attachment=False
        )
        os.remove("inference_pipeline.log")
        return response
    except Exception:
        return jsonify({"error": "Could not read log file"}), 500


@app.route("/get_logs")
def get_logs():
    try:
        shutil.copy("logs/inference_pipeline.log", "inference_pipeline.log")
        response = send_file("inference_pipeline.log", as_attachment=True)
        os.remove("inference_pipeline.log")
        return response
    except Exception:
        return jsonify({"error": "Could not read log file"}), 500


@app.route("/show_data_logs")
def show_data_logs():
    try:
        return send_file("logs/features_prediction.csv", as_attachment=False)
    except Exception:
        return jsonify({"error": "Could not read log file"}), 500


@app.route("/get_data_logs")
def get_data_logs():
    try:
        return send_file("logs/features_prediction.csv", as_attachment=True)
    except Exception:
        return jsonify({"error": "Could not read log file"}), 500


@app.route("/predict", methods=["POST"])
def predict():
    # clinet authentication
    auth_token = request.headers.get("auth_token")
    client_uid = request.headers.get("client_uid")
    if check_client_auth(client_uid, auth_token):
        return {'message': 'Unauthorized'}, 401
    
    # get image file
    if 'image' not in request.files:
        return {'message': 'No file part'}, 400
    file = request.files['image']
    if file.filename == '':
        return {'message': 'No selected file'}, 400

    # check if file is jpg
    if not file.filename.endswith(('.jpg', '.jpeg')):
        return {'message': 'Filetype not supported.'}, 400

    # get sensor value
    sensor_value = request.form.get("sensor_value")
    if sensor_value is None:
        sensor_value = 0

    # run inference pipeline
    prediction = inference_pipeline.run(file, sensor_value)

    return {'prediction': prediction}, 200
