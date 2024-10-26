from inference_pipeline import InferencePipeline  # noqa: F401
from clients import create_client, check_client_auth
from clients import get_client_model, set_client_model
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
    client_uid = request.form.get("client_uid")
    auth_token = request.headers.get("Authorization")
    if client_uid is None or auth_token is None:
        return {'message': 'Missing credetials'}, 401
    if not check_client_auth(client_uid, auth_token):
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


@app.route("/create_client", methods=["POST"])
def create_client_route():
    # get client name
    client_name = request.form.get("name")
    if client_name is None:
        return {'message': 'No client name specified.'}, 400

    # create client
    uid, auth_token = create_client(client_name)

    return {'client_uid': uid, 'auth_token': auth_token}, 200


@app.route("/set_model_version", methods=["POST"])
def set_model_version_route():
    # get client info
    client_uid = request.form.get("client_uid")
    if client_uid is None:
        return {'message': 'No client specified.'}, 400

    # get model name and version
    model_name = request.form.get("model_name")
    if model_name is None:
        return {'message': 'Missing model name'}, 400
    model_version = request.form.get("model_version")
    if model_version is None:
        return {'message': 'Missing model version.'}, 400

    # set model for client
    set_client_model(client_uid, model_name, model_version)

    return {'message': 'Model set successfully'}, 200


@app.route("/get_model_version", methods=["POST"])
def get_model_version_route():
    # get client info
    client_uid = request.form.get("client_uid")
    if client_uid is None:
        return {'message': 'No client specified.'}, 400

    # get model for client
    model, version = get_client_model(client_uid)
    if model is None or version is None:
        return {'messsage': 'Unknown client'}, 400

    return {'model_name': model, 'model_version': version}, 200
