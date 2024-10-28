user_roles = None
def acces_control(roles):

    def decorator(func):
        def wrapper(*args, **kwargs):
            if not any(role in user_roles for role in roles):
                raise PermissionError("Отказано в доступе. Ни одна из ролей пользователя не имеет соответствующих прав.")
            return func(*args, **kwargs)
        return wrapper
    return decorator


@acces_control(roles=['admin', 'moderator'])
def some_func():
    print("Доступ открыт")


try:
    user_roles = 'admin'
    some_func()
except PermissionError as e:
    print(e)

