from pipeline import InferencePipeline  # noqa: F401
from tables.clients import create_client, check_client_auth
from tables.clients import list_clients, delete_client
from tables.deployments import create_deployment, list_deployments
from tables.deployments import set_active_deployment, get_active_deployment
from tables.deployments import delete_deployment
from helpers.email import send_email
from flask import Flask, request, jsonify, send_file
import shutil
import os

app = Flask(__name__)

inference_pipeline = InferencePipeline()


@app.route("/")
def index_route():
    return """
        <h1>Inference API is running</h1>
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


@app.route("/predict", methods=["POST"])
def predict_route():
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


@app.route("/list_clients", methods=["POST"])
def list_clients_route():
    clients = list_clients()
    return {'message': clients}, 200


@app.route("/delete_client", methods=["POST"])
def delete_client_route():
    # get client info
    client_uid = request.form.get("client_uid")
    if client_uid is None:
        return {'message': 'No client specified.'}, 400

    # delete client
    success = delete_client(client_uid)
    if not success:
        return {'message': 'Unknown client'}, 400
    return {'message': 'Successfully deleted client'}, 200


@app.route("/create_deployment", methods=["POST"])
def create_deployment_route():
    # get inputs
    deployment_name = request.form.get("name")
    if deployment_name is None:
        return {'message': 'No deployment name specified.'}, 400
    model_name = request.form.get("model_name")
    if model_name is None:
        return {'message': 'No model name specified.'}, 400
    model_version = request.form.get("model_version")
    if model_version is None:
        return {'message': 'No model version specified.'}, 400

    # create deployment
    uid = create_deployment(deployment_name, model_name, model_version)

    return {'deployment_uid': uid}, 200


@app.route("/list_deployments", methods=["POST"])
def list_deployments_route():
    deployments = list_deployments()
    return {'message': deployments}, 200


@app.route("/get_active_deployment", methods=["POST"])
def get_active_deployment_route():
    name, model, version = get_active_deployment()
    if name is None:
        return {'message': 'No active deployment'}, 400
    return {
        'deployment_name': name,
        'model_name': model,
        'model_version': version
    }, 200


@app.route("/set_active_deployment", methods=["POST"])
def set_active_deployment_route():
    # get deployment info
    deployment_uid = request.form.get("deployment_uid")
    if deployment_uid is None:
        return {'message': 'No deployment specified.'}, 400

    # set deployment
    success = set_active_deployment(deployment_uid)
    if not success:
        return {'message': 'Unknown deployment or already active'}, 400
    return {'message': 'Deployment set successfully'}, 200


@app.route("/delete_deployment", methods=["POST"])
def delete_deployemnt_route():
    # get deployment info
    deployment_uid = request.form.get("deployment_uid")
    if deployment_uid is None:
        return {'message': 'No deployment specified.'}, 400

    # delete deployment
    success = delete_deployment(deployment_uid)
    if not success:
        return {'message': 'Unknown deployment'}, 400
    return {'message': 'Successfully deleted deployment'}, 200


@app.route("/send_email", methods=["POST"])
def send_email_route():
    if send_email("Updates von Inference API", "Es gibt neue Updates."):
        return {'message': 'Email sent successfully'}, 200
    return {'message': 'Failed to send email'}, 500
