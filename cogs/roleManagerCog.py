import discord, asyncio
import data.quotes as quotes, utils.genUtils as genUtils
from data.localdata import serverId, leerkrachtRoleId, countryRoleColor
from discord import Interaction, Member, app_commands
from discord.ext import commands
from utils.genUtils import isStaff
from modules.roleManager.roleManager import *
from discord.app_commands import Choice
from fuzzywuzzy import fuzz
from discord.ext.commands import CommandError

AssertionError = CommandError

class roleManagerCog(commands.Cog):
    def __init__(self, bot):
        self.bot: discord.Client = bot
        self.rolesPendingRemoval: list[PendingEntry] = getRolesPendingRemoval()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Role Manager Cog is ready")

        queue = queuePendingRemovals(self.bot.get_guild(serverId), self.rolesPendingRemoval)
        if len(queue) > 0: await asyncio.gather(*queue, return_exceptions=True)

    @app_commands.command(name="giveleerkrachtrole", description="Geef de leerkracht rol aan iemand")
    @app_commands.describe(user="username", duration="duration in minutes")
    @genUtils.catcherrors
    async def giveleerkrachtrole(self, i9n: Interaction, user: Member, duration: int = 180) -> None:
        assert isStaff(i9n.user), quotes.NOT_STAFF_ERROR
        await giveTemporaryRole(self.rolesPendingRemoval, i9n, user, i9n.guild.get_role(leerkrachtRoleId), duration)

    @app_commands.command(name="landrol", description="Assign country roles")
    @app_commands.describe(land="De naam van het land")
    @genUtils.catcherrors
    async def landrol(self, i9n: discord.Interaction, land: str):
        responseMsg = "Alsjeblieft!"
        await i9n.user.add_roles([role for role in i9n.guild.roles if role.name == land][0])
        await i9n.response.send_message(responseMsg)

    @landrol.autocomplete('land')
    async def landrol_autocomplete(self, i9n: discord.Interaction, current: str):
        try: 
            roles = sorted(
                [role.name for role in i9n.guild.roles if role.color == countryRoleColor], 
                key=(lambda role: fuzz.ratio(role.lower(), current.lower())), 
                reverse=True
            )
            return [Choice(name=role, value=role) for role in roles[:10]] 
        except Exception as e: print(e)

    @app_commands.command(name="niveaurol", description="Assign level roles")
    @genUtils.catcherrors
    async def niveaurol(self, i9n: discord.Interaction):
        await i9n.user.remove_roles(*[role for role in i9n.user.roles if "Niveau" in role.name])
        view = await roleSelectionView(i9n.guild, lambda x:("Niveau" in x.name) and not ("C+" in x.name), 1)
        await i9n.response.send_message("Here you go!", view=view)

async def setup(bot):
    await bot.add_cog(roleManagerCog(bot), guilds=[discord.Object(id=serverId)])

### IGNORE FOR NOW ###
        # channel = self.bot.get_channel(channelID)
        # role = channel.guild.get_role(roleID)
        # today = dt.datetime.now(dt.timezone.utc)

        # def getHistory(): 
        #     return channel.history(limit=None, after=today - dt.timedelta(days=60))

        # users = set([msg.author async for msg in getHistory()])

        # for user in set(role.members).difference(users): 
        #     await user.remove_roles(role)

        # warnedUsers = []
        # async for message in getHistory():
        #     user = message.author

        #     if (today - message.created_at).days != 30: continue
        #     if user not in role.members or user in warnedUsers: continue

        #     await user.send("U r dum")
        #     warnedUsers.append(user)