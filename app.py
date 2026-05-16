import os

def read_secret(path):
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except:
        return "NO_SECRET"

@app.route("/")
def home():
    app_env = os.getenv("APP_ENV", "DEV")
    app_version = os.getenv("APP_VERSION", "unknown")
    secret = read_secret("/run/secrets/app_secret")

    return f"""
    <h1>Hello from Docker Swarm!</h1>
    <p><b>Environment:</b> {app_env}</p>
    <p><b>Version:</b> {app_version}</p>
    <p><b>Secret:</b> {secret}</p>
    <p><b>Host:</b> {socket.gethostname()}</p>
    """
