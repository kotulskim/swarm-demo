from flask import Flask
import socket
import os
import psycopg2
import redis
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



redis_client = redis.Redis(
    host='redis',
    port=6379,
    decode_responses=True
)

from flask import request

@app.before_request
def log_request():
    with open("/shared-logs/access.log", "a") as f:
        f.write(
            f"{request.method} {request.path} handled by {socket.gethostname()}\n"
        )

@app.route("/")
def home():
    return f"Hello from {socket.gethostname()} v9"

@app.route("/redis-count")
def redis_count():
    count = redis_client.incr("counter")
    return f"Redis counter: {count}\n"


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

@app.route("/job")
def create_job():
    job_id = redis_client.incr("job_id")
    payload = f"job-{job_id}"

    redis_client.rpush("jobs", payload)

    return f"Job created: {payload}\n"


@app.route("/jobs-done")
def jobs_done():
    count = redis_client.get("jobs_done") or 0
    return f"Jobs done: {count}\n"


app.run(host="0.0.0.0", port=5005)
