import redis
from datetime import timedelta
from functools import wraps

def single(max_processing_time: timedelta = 0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

            lock_name = f'lock_{func.__name__}'
            lock = redis_client.lock(lock_name, timeout=max_processing_time.total_seconds())

            if lock.acquire(blocking=False):
                try:
                    return func(*args, **kwargs)
                finally:
                    lock.release()
            else:
                raise Exception("Функция уже используется")
        return wrapper
    return decorator