# с помощью метаклассов

class SingletonMeta(type):

    __instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super().__call__(*args, **kwargs)
        return cls.__instances[cls]

class MyClass(metaclass=SingletonMeta):
    pass

obj1 = MyClass()
obj2 = MyClass()

print(obj1 is obj2)

# с помощью метода __new__ класса

class Singleton():
    __instances = None

    def __new__(cls, *args, **kwargs):
        if cls.__instances is None:
            cls.__instances = super().__new__(cls)
        return cls.__instances
    



