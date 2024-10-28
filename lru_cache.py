import unittest.mock


def lru_cache(*args, **kwargs):
    maxsize = kwargs.get('maxsize', None)

    def decorator(func):
        cache = {}

        def make_key(*args, **kwargs):
            try:
                for arg in args:
                    hash(arg) 
                for key in kwargs:
                    hash(key)
            except TypeError:
                raise ValueError("Данные объекты не могут быть использованы в качестве ключей.")
            return (args, frozenset(kwargs.items()))

        def wrapper(*args, **kwargs):
            key = make_key(*args, **kwargs)
            if key in cache:
                return cache[key]
            
            result = func(*args, **kwargs)

            cache[key] = result

            if maxsize is not None and len(cache) > maxsize:
                oldest_key = next(iter(cache)) 
                del cache[oldest_key]
            
            return result
        
        return wrapper
    
    if len(args) == 1 and callable(args[0]):
        return decorator(args[0])
    else:
        return decorator


@lru_cache
def sum(a: int, b: int) -> int:
    return a + b


@lru_cache
def sum_many(a: int, b: int, *, c: int, d: int) -> int:
    return a + b + c + d


@lru_cache(maxsize=3)
def multiply(a: int, b: int) -> int:
    return a * b


if __name__ == '__main__':
    
    assert sum(1, 2) == 3
    assert sum(3, 4) == 7

    assert multiply(1, 2) == 2
    assert multiply(3, 4) == 12

    assert sum_many(1, 2, c=3, d=4) == 10

    mocked_func = unittest.mock.Mock()
    mocked_func.side_effect = [1, 2, 3, 4]

    decorated = lru_cache(maxsize=2)(mocked_func)
    assert decorated(1, 2) == 1
    assert decorated(1, 2) == 1
    assert decorated(3, 4) == 2
    assert decorated(3, 4) == 2
    assert decorated(5, 6) == 3
    assert decorated(5, 6) == 3
    assert decorated(1, 2) == 4
    assert mocked_func.call_count == 4