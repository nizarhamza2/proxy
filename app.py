from flask import Flask, request, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

FIREBASE_URL = "https://your-project.firebaseio.com/sensor.json"
AUTH_TOKEN = os.getenv("AUTH_TOKEN", "mysecrettoken")  # Optional security

@app.route("/post", methods=["POST"])
def post_data():
    # Optional simple token check
    token = request.headers.get("Authorization")
    if token != f"Bearer {AUTH_TOKEN}":
        return jsonify({"error": "Unauthorized"}), 401

    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({"error": "No JSON"}), 400

        json_data["timestamp"] = datetime.utcnow().isoformat() + "Z"
        fb_response = requests.post(FIREBASE_URL, json=json_data)
        return jsonify({"firebase_status": fb_response.status_code})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def index():
    return "Firebase Proxy is running.", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

