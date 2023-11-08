import pickle

from flask import Flask
from flask import request
from flask import jsonify
import pandas as pd

def load(filename: str):
    with open(filename, 'rb') as f_in:
        return pickle.load(f_in)


model = load('rfc_model.bin')

app = Flask('midterm-ml')


@app.route('/predict', methods=['POST'])
def predict():
    climate = request.get_json()
    X = pd.DataFrame([climate])

    y_pred = model.predict_proba(X)[0, 1]
    get_score = y_pred >= 0.5

    result = {
        'frogs_presence_probability': float(y_pred),
        'frogs_presence_score': bool(get_score)
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)