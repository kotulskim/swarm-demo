from flask import Flask
import socket

app = Flask(__name__)

@app.route("/")
def home():
    return f"Hello from Docker Swarm v2! Host: {socket.gethostname()}"

@app.route("/health")
def health():
    return "OK", 200

app.run(host="0.0.0.0", port=5005)
