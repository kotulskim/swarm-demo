import time
import redis
import os

redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

print("Worker started. Waiting for jobs...")

while True:
    job = redis_client.blpop("jobs", timeout=5)

    if job:
        queue_name, payload = job
        print(f"Received job: {payload}")

        time.sleep(5)

        redis_client.incr("jobs_done")
        print(f"Finished job: {payload}")
    else:
        print("No jobs...")
