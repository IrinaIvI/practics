from datetime import datetime

class MetaTime(type):

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls, *args, **kwargs)
        instance.created_at = datetime.now().strftime('%Y-%m-%d %H:%M')
        return instance

class MyClass(metaclass=MetaTime):
    pass

obj = MyClass()

print(obj.created_at)