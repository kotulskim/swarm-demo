from flask import Flask
import socket
import os

app = Flask(__name__)

@app.route("/")
def home():
    app_env = os.getenv("APP_ENV", "DEV")
    app_version = os.getenv("APP_VERSION", "unknown")

    return f"""
    <h1>Hello from Docker Swarm!</h1>
    <p><b>Environment:</b> {app_env}</p>
    <p><b>Version:</b> {app_version}</p>
    <p><b>Host:</b> {socket.gethostname()}</p>
    """

@app.route("/health")
def health():
    return "OK", 200

app.run(host="0.0.0.0", port=5005)
