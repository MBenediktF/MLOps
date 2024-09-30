from .run_inference_pipeline import run_inference_pipeline
from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    input = request.get_json()
    features = pd.DataFrame.from_dict(input)

    prediction = run_inference_pipeline(features)

    return jsonify({'prediction': prediction})
