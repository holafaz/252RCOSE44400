from flask import Flask, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

DATA_PATH = "/data/message.txt"


def read_message():
    """Return stored message or empty string."""
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""


def write_message(msg: str):
    """Write message with timestamp to file."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full = f"{msg} (updated at {now})"
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        f.write(full)


@app.route("/api/message", methods=["GET"])
def get_message():
    msg = read_message()
    return jsonify({"message": msg})


@app.route("/api/message", methods=["POST"])
def update_message():
    data = request.get_json() or {}
    msg = data.get("message", "")

    write_message(msg)

    return jsonify({"status": "ok", "message": msg}), 201


# (V2 will add timestamp + /api/health later)

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

