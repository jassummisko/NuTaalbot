import functools, yaml
from discord.ext.commands import CommandError
from discord import Interaction, Member
from discord.ext import menus

def catcherrors(func):
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

def loadYaml(path: str) -> dict:
    with open(path) as file:
        return yaml.load(file, Loader=yaml.Loader)

def saveYaml(dict: dict, path: str):
    with open(path, "w") as file:
        file.write(yaml.dump(dict))

class MultiPageEmbed(menus.ListPageSource):
    async def format_page(self, menu, page):
        return page