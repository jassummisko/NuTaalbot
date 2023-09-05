import functools, yaml
from taalbot import BOT
from re import error
from data.localdata import logChannelId
from discord.ext.commands import CommandError, Context
from discord import Interaction, Member, message
import discord
from discord.ext import menus # type: ignore

def catcherrors(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        culprit: Interaction | Context = args[1]

        try: await func(*args, **kwargs)
        except CommandError as e: 
            if isinstance(args[1], Interaction):
                await args[1].response.send_message(e.args[0], ephemeral=True)
        except Exception as e: 
            assert isinstance(
                (logChannel := BOT.get_channel(logChannelId)), 
                discord.TextChannel
            )

            if isinstance(args[1], Context): user = args[1].author
            else: user = args[1].user

            authorId = user.id
            authorName = user.name
            authorDisplayName = user.display_name
            extraInfo: list[tuple[str, str]] = []
            errorMessage = str(e)
            if culprit.command: extraInfo.append(("Command called", culprit.command.name))
            if len(errorMessage := str(e)) > 1500:
                errorMessage = "Error message too long, please log onto the server hosting the bot and read it."

            messageFormat = f"""**ERROR REPORT**: User `{authorName}`, with display name `{authorDisplayName}` and ID `{authorId}` invoked an interaction and caused an error."""
            for entry in extraInfo: messageFormat += f"\n__{entry[0]}__: `{entry[1]}`"
            messageFormat += f"\n__Error message__: `{errorMessage}`"
            messageFormat += f"\n\nIf the bot is still online, there is probably no reason to panic. These reports are just to help the bot devs know when something has gone wrong."

            await logChannel.send(messageFormat)
            print(e)

    return wrapper

def mentionToId(mention: str) -> int:
    user_id = mention \
        .removeprefix("<@") \
        .removesuffix(">")
    return int(user_id)

def isStaff(user: Member):
    from data.localdata import staffRoles
    staffRoleIDs = [staffRole.value for staffRole in staffRoles]
    return len(set([role.id for role in user.roles]).intersection(staffRoleIDs))>0 

def loadYaml(path: str) -> dict:
    with open(path) as file:
        return yaml.load(file, Loader=yaml.Loader)

def saveYaml(dict: dict, path: str):
    with open(path, "w") as file:
        file.write(yaml.dump(dict))

class MultiPageEmbed(menus.ListPageSource):
    async def format_page(self, _, page):
        return page