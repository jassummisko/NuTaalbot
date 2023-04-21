import functools, yaml
from discord.ext.commands import CommandError
from discord import Interaction, Member

AssertionError = CommandError

def catcherrors(func: callable):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        i9n: Interaction = args[1]
        try: await func(*args, **kwargs)
        except CommandError as e: await i9n.response.send_message(e.args[0], ephemeral=True)
        except Exception as e: print(e)
    return wrapper

def isStaff(user: Member):
    from data.dataIds import staffRoles
    staffRoleIDs = [staffRole.value for staffRole in staffRoles]
    return len(set([role.id for role in user.roles]).intersection(staffRoleIDs))>0 

def loadYaml(path: str):
    with open(path) as file:
        return yaml.load(file, Loader=yaml.Loader)

def saveYaml(dict: dict, path: str):
    with open(path, "w") as file:
        file.write(yaml.dump(dict))

def lev_dist(a: str, b: str) -> int:
    @functools.lru_cache(None) 
    def min_dist(s1, s2):
        if s1 == len(a) or s2 == len(b): return len(a) - s1 + len(b) - s2
        if a[s1] == b[s2]: return min_dist(s1 + 1, s2 + 1)
        return 1 + min(
            min_dist(s1, s2 + 1),      # insert character
            min_dist(s1 + 1, s2),      # delete character
            min_dist(s1 + 1, s2 + 1),  # replace character
        )

    return min_dist(0, 0)
