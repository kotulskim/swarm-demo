from flask import Flask
import socket
import os
import psycopg2

app = Flask(__name__)

def read_secret(path):
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except:
        return None

def get_db_connection():
    password = read_secret("/run/secrets/db_password")

    return psycopg2.connect(
        host="postgres",
        database="appdb",
        user="appuser",
        password=password
    )

@app.route("/")
def home():
    return f"Hello from {socket.gethostname()}"

@app.route("/init")
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS visits (count INT);")
    cur.execute("INSERT INTO visits (count) VALUES (1);")

    conn.commit()
    cur.close()
    conn.close()

    return "DB initialized"

@app.route("/count")
def count():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM visits;")
    result = cur.fetchone()[0]

    cur.close()
    conn.close()

    return f"Rows in DB: {result}"

@app.route("/health")
def health():
    return "OK", 200

app.run(host="0.0.0.0", port=5005)
