import json
import redis

redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)


class RedisQueue:

    def __init__(self, redis_client: redis.StrictRedis, name="default"):
        """Инициализация очереди."""
        self.redis_client = redis_client
        self.name = name

    def publish(self, msg: dict):
        """Добавление сообщений в очередь."""
        serialized_msg = json.dumps(msg)
        self.redis_client.rpush(self.name, serialized_msg)

    def consume(self) -> dict:
        """Извлечение сообщений из очереди."""
        serialized_msg = self.redis_client.lpop(self.name)
        if serialized_msg is None:
            return None
        result = json.loads(serialized_msg)
        return result


if __name__ == "__main__":
    q = RedisQueue()
    q.publish({"a": 1})
    q.publish({"b": 2})
    q.publish({"c": 3})

    assert q.consume() == {"a": 1}
    assert q.consume() == {"b": 2}
    assert q.consume() == {"c": 3}
