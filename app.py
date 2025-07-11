from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

FIREBASE_URL = "https://your-project.firebaseio.com/sensor.json"

@app.route("/post", methods=["POST"])
def post_data():
    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({"error": "No JSON"}), 400

        fb_response = requests.put(FIREBASE_URL, json=json_data)
        return jsonify({"firebase_status": fb_response.status_code})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def index():
    return "Firebase Proxy is running.", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

