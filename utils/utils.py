import functools, yaml
from discord.ext.commands import CommandError

def catcherrors(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        ctx, errorMessage = args[1], e.args[0]
        try: await func(*args, **kwargs)
        except CommandError as e: await ctx.send(errorMessage)         
        except Exception as e: print(e)
    return wrapper

def isStaff(user):
    from data import staffRoles
    staffRoleIDs = [staffRole.value for staffRole in staffRoles]
    return len(set([role.id for role in user.roles]).intersection(staffRoleIDs))>0 

def loadYaml(path):
    with open(path) as file:
        return yaml.load(file, Loader=yaml.Loader)

def saveYaml(dict, path):
    with open(path, "w") as file:
        file.write(yaml.dump(dict))

