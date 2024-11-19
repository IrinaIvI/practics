import random
import time
import redis
from datetime import datetime

redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)


class RateLimitExceed(Exception):
    pass


class RateLimiter:
    def __init__(self, redis_client: redis.StrictRedis, name="default"):
        self.redis_client = redis_client
        self.name = name
        self.max_requests = 5

    def test(self) -> bool:
        messages = self.redis_client.lrange(self.name, 0, -1)
        if not messages:
            return True
        messages = [float(msg.decode()) for msg in messages]
        current_time = datetime.now().timestamp()

        while messages and messages[0] > current_time - 3:
            self.redis_client.lpop(self.name)

        messages = self.redis_client.lrange(self.name, 0, -1)

        if len(messages) < self.max_requests:
            self.redis_client.rpush(self.name, current_time)
            return True
        return False


def make_api_request(rate_limiter: RateLimiter):
    if not rate_limiter.test():
        raise RateLimitExceed
    else:
        # какая-то бизнес логика
        pass


if __name__ == "__main__":
    rate_limiter = RateLimiter(redis_client)

    for _ in range(50):
        time.sleep(random.randint(1, 2))

        try:
            make_api_request(rate_limiter)
        except RateLimitExceed:
            print("Rate limit exceed!")
        else:
            print("All good")
