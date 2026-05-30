import time
import redis

redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True,
    socket_timeout=10,
    socket_connect_timeout=5,
)

print("Worker started. Waiting for jobs...", flush=True)

while True:
    try:
        job = redis_client.blpop("jobs", timeout=5)

        if job:
            queue_name, payload = job
            print(f"Received job: {payload}", flush=True)

            time.sleep(5)

            redis_client.incr("jobs_done")
            print(f"Finished job: {payload}", flush=True)
        else:
            print("No jobs...", flush=True)

    except redis.exceptions.TimeoutError:
        print("Redis timeout while waiting for job. Retrying...", flush=True)
        time.sleep(2)

    except redis.exceptions.ConnectionError as e:
        print(f"Redis connection error: {e}. Retrying...", flush=True)
        time.sleep(5)
