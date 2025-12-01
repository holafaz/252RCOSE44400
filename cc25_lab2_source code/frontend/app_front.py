from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

BACKEND_URL = "http://backend:5001"


@app.route("/", methods=["GET"])
def index():
    try:
        r = requests.get(f"{BACKEND_URL}/api/message", timeout=3)
        msg = r.json().get("message", "")
    except:
        msg = "Error contacting backend"

    #default
    msg_only = msg

    # Parse timestamp from pattern " (updated at YYYY-MM-DD HH:MM:SS)"
    last_updated = ""
    marker = " (updated at "
    if marker in msg and msg.endswith(")"):

        msg_only=msg.split(marker)[0]
        start = msg.rfind(marker) + len(marker)
        end = len(msg) - 1  # drop trailing ")"
        last_updated = msg[start:end]

    return render_template(
        "index.html",
        current_message=msg_only,
        last_updated=last_updated,
    )




@app.route("/update", methods=["POST"])
def update():
    new_msg = request.form.get("new_message", "")

    try:
        requests.post(
            f"{BACKEND_URL}/api/message",
            json={"message": new_msg},
            timeout=3
        )
    except:
        pass

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


