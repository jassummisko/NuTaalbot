import functools, yaml

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
    staffRoleIDs = [staffRole.value for staffRole in staffRoles]
    return len(set([role.id for role in user.roles]).intersection(staffRoleIDs))>0 

def loadYaml(path):
    with open(path) as file:
        return yaml.load(file, Loader=yaml.Loader)