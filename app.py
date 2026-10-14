import os
import time

import redis
from flask import Flask

app = Flask(__name__)

STUDENT_NAME = os.getenv("STUDENT_NAME", "unknown")  # set with: -e STUDENT_NAME=Saira
ROLL = os.getenv("ROLL", "unknown")                  # set with: -e ROLL=55503
REDIS_HOST = os.getenv("REDIS_HOST", "redis")        # service name in docker-compose.yml

cache = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)


def count_hit(retries=3):
    """Increase the 'hits' counter stored in Redis (retry briefly if Redis is still starting)."""
    while True:
        try:
            return cache.incr("hits")
        except redis.exceptions.ConnectionError:
            if retries == 0:
                raise
            retries -= 1
            time.sleep(0.3)


@app.route("/")
def index():
    try:
        hits = count_hit()
        msg = f"Hello from {STUDENT_NAME} (Roll No: {ROLL})! This page has been viewed {hits} time(s).\n"
    except redis.exceptions.RedisError:
        msg = f"Hello from {STUDENT_NAME} (Roll No: {ROLL})! (Redis is not reachable, so no counter)\n"
    print(msg.strip(), flush=True)                   # shows up in: docker logs <container>
    return msg


@app.route("/health")
def health():
    return "ok\n"


if __name__ == "__main__":
    print(f"Starting app for {STUDENT_NAME}, roll number: {ROLL}", flush=True)
    app.run(host="0.0.0.0", port=5000)               # 0.0.0.0 so it is reachable via -p