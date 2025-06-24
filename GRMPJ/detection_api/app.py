from flask import Flask, request, jsonify
import os

from detector import detect_risk
from reporter import generate_report

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "default_secret_key")

THRESHOLD = 0.8

@app.route('/analyze', methods=['POST'])
def predict():
    data = request.get_json()
    room_id = data.get("room_id")
    messages = data.get("messages")

    if not messages:
        return jsonify({"error": "No messages provided"}), 400

    risk = detect_risk(messages)

    result = {"risk": risk}
    if risk >= THRESHOLD:
        report = generate_report(room_id, messages, risk)
        result["report"] = report

    return jsonify(result)

if __name__ == '__main__':
    DEBUG = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    PORT = int(os.environ.get("PORT", 5000))
    app.run(debug=DEBUG, host="0.0.0.0", port=PORT)