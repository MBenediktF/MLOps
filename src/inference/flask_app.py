from run_inference_pipeline import run_inference_pipeline
from flask import Flask, request, jsonify, send_file
import pandas as pd
import shutil
import os

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
    input = request.get_json()
    features = pd.DataFrame.from_dict(input)

    prediction = run_inference_pipeline(features)

    return jsonify({"prediction": prediction})


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return {'message': 'No file part'}, 400

    file = request.files['file']

    if file.filename == '':
        return {'message': 'No selected file'}, 400

    if file:
        file_path = os.path.join('images', file.filename)
        file.save(file_path)
        return {'message': 'File uploaded successfully'}, 200
