from flask import Flask, request, jsonify
import joblib
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
model = joblib.load('upi_fraud_detection_model.pkl')  # Load your trained model

@app.route('/api/detect-fraud', methods=['POST'])
def detect_fraud():
    data = request.json
    # Preprocess the input data
    input_data = {
        'upi_id': [data['upiId']],
        'amount': [data['amount']],
    }
    input_df = pd.DataFrame(input_data)
    input_df['upi_id'] = input_df['upi_id'].astype('category').cat.codes  # Encode UPI ID

    # Predict using the model
    prediction = model.predict(input_df)
    return jsonify({'result': 'Fraud' if prediction[0] == 1 else 'No Fraud'})

if __name__ == '__main__':
    app.run(debug=True)
