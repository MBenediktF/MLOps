from run_inference_pipeline import run_inference_pipeline
from flask import Flask, request, jsonify, send_file
import pandas as pd
import shutil

app = Flask(__name__)


@app.route('/')
def index():
    return '''
        <h1>Inference API is running</h1>
        <ul>
            <li><a href="/show_logs">Logs</a></li>
            <li><a href="/show_data_logs">Data Logs</a></li>
        </ul>
    '''


@app.route('/show_logs')
def show_logs():
    try:
        shutil.copy('inference_pipeline.log', 'export_inference_pipeline.log')
        return send_file('export_inference_pipeline.log',
                         mimetype='text/plain',
                         as_attachment=False)
    except Exception:
        return jsonify({'error': 'Could not read log file'}), 500


@app.route('/show_data_logs')
def show_data_logs():
    try:
        return send_file('features_prediction_log.csv', as_attachment=False)
    except Exception:
        return jsonify({'error': 'Could not read log file'}), 500


@app.route('/predict', methods=['POST'])
def predict():
    input = request.get_json()
    features = pd.DataFrame.from_dict(input)

    prediction = run_inference_pipeline(features)

    return jsonify({'prediction': prediction})
