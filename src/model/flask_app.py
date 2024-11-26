from helpers.logs import Log  # noqa: F401
from flask import Flask, request, jsonify, send_file
import shutil
import os
import json
from create_dataset import create_dataset_from_measurements
from tables.datasets import list_datasets
from flask_cors import CORS

log = Log()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/")
def index_route():
    return """
        <h1>Model services API is running</h1>
        <ul>
            <li><a href="/show_logs">Show Logs</a></li>
            <li><a href="/get_logs">Download Logs</a></li>
        </ul>
    """


@app.route("/show_logs")
def show_logs_route():
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
def get_logs_route():
    try:
        shutil.copy("logs/inference_pipeline.log", "inference_pipeline.log")
        response = send_file("inference_pipeline.log", as_attachment=True)
        os.remove("inference_pipeline.log")
        return response
    except Exception:
        return jsonify({"error": "Could not read log file"}), 500


@app.route("/create_dataset", methods=["POST"])
def create_dataset():
    # get measurement name
    measurements = request.form.get("measurements")
    measurements = json.loads(measurements) if measurements else []
    if measurements is None or measurements == []:
        return {'message': 'No measurement name.'}, 400
    # create dataset
    dataset_uid, num_images = create_dataset_from_measurements(measurements)
    responseString = f'Created dataset {dataset_uid}, {num_images} images'
    return {'message': responseString}, 200


@app.route("/list_datasets", methods=["POST"])
def list_datasets_route():
    datasets = list_datasets()
    return {'message': datasets}, 200
