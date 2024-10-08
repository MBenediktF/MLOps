from run_inference_pipeline import run_inference_pipeline
from flask import Flask, request, jsonify, send_file
import shutil
import os
from log_features_prediction import log_features_prediction, file_is_jpg
from create_dataset import create_dataset_from_measurement

app = Flask(__name__)


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
    # get image file
    if 'image' not in request.files:
        return {'message': 'No file part'}, 400
    file = request.files['image']
    if file.filename == '':
        return {'message': 'No selected file'}, 400
    if not file_is_jpg(file):
        return {'message': 'Filetype not supported.'}, 400

    # get sensor value
    sensor_value = request.form.get("sensor_value")
    if sensor_value is None:
        return {'message': 'No sensor value provided.'}, 400

    # prediction = run_inference_pipeline(features)
    prediction = 44

    try:
        log_features_prediction(file, prediction, sensor_value)
    except Exception as e:
        return {'message': f'Could not store data: {e}'}, 500

    return {'prediction': prediction}, 200


@app.route("/create_dataset", methods=["POST"])
def create_dataset():
    # get measurement name
    measurement = request.form.get("measurement")
    if measurement is None:
        return {'message': 'No measurement name.'}, 400
    dataset_uuid, num_images = create_dataset_from_measurement(measurement)
    responseString = f'Created dataset {dataset_uuid}, {num_images} images'
    return {'message': responseString}, 200
