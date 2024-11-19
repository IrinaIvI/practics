
import redis
import json
class RedisQueue:
    def __init__(self, name='default'):
        self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.name = name

    def publish(self, msg: dict):
        serialized_msg = json.dumps(msg)
        self.redis_client.rpush(self.name, serialized_msg)

    def consume(self) -> dict:
        serialized_msg = self.redis_client.lpop(self.name)
        result = json.loads(serialized_msg)
        return result


if __name__ == '__main__':
    q = RedisQueue()
    q.publish({'a': 1})
    q.publish({'b': 2})
    q.publish({'c': 3})

    assert q.consume() == {'a': 1}
    assert q.consume() == {'b': 2}
    assert q.consume() == {'c': 3}

