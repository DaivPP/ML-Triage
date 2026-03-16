from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib

app = Flask(__name__)

# Load model
model = joblib.load("triage_model.pkl")
scaler = joblib.load("scaler.pkl")

numeric_features = [
    "age", "heart_rate", "spo2",
    "systolic_bp", "respiratory_rate",
    "temperature"
]

triage_map = {
    0: "Non-Urgent",
    1: "Urgent",
    2: "Critical"
}

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    input_data = pd.DataFrame([data])

    input_data[numeric_features] = scaler.transform(
        input_data[numeric_features]
    )

    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)[0]
    confidence = max(probabilities)

    triage_level = triage_map[prediction]

    return jsonify({
        "triage": triage_level,
        "confidence": round(confidence * 100, 2)
    })


if __name__ == "__main__":
    app.run(debug=True)