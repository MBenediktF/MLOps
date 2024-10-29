from helpers.logs import log_message  # noqa: F401
from flask import Flask, request, jsonify, send_file
import shutil
import os
from run_experiment import run_experiment, check_parameter_grid
import threading
import json
from create_dataset import create_dataset_from_measurement


app = Flask(__name__)


@app.route("/")
def index_route():
    return """
        <h1>Model training API is running</h1>
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
    measurement = request.form.get("measurement")
    if measurement is None:
        return {'message': 'No measurement name.'}, 400
    # create dataset
    dataset_uuid, num_images = create_dataset_from_measurement(measurement)
    responseString = f'Created dataset {dataset_uuid}, {num_images} images'
    return {'message': responseString}, 200


@app.route("/run_experiment", methods=["POST"])
def run_experiment_route():
    # get and check parameters
    experiment_name = request.form.get("experiment_name")
    if experiment_name is None:
        return {'message': 'No experiment name.'}, 400

    dataset_id = request.form.get("dataset_id")
    if dataset_id is None:
        return {'message': 'No dataset id.'}, 400

    test_split = request.form.get("test_split")
    if test_split is None:
        test_split = 0.2
    try:
        test_split = float(test_split)
    except Exception as e:
        return {'message': str(e)}, 400

    parameters = request.form.get("parameters")
    if parameters is None:
        return {'message': 'No parameters.'}, 400
    try:
        parameters = json.loads(parameters)
        check_parameter_grid(parameters)
    except Exception as e:
        return {'message': str(e)}, 400

    # start training thread
    experiment_thread = threading.Thread(
        target=run_experiment,
        args=(experiment_name, dataset_id, test_split, parameters))
    experiment_thread.start()
    responseString = f'Started experiment {experiment_name}.'
    return {'message': responseString}, 200
