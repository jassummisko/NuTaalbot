import functools

def tryexcept(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            await func(*args, **kwargs)
        except Exception as e:
            print(e)

    return wrapper

def isStaff(user):
    from data import staffRoles
    for role in user.roles:
        if role.id in staffRoles:
            return True
    return False