import discord, asyncio
import data.quotes as quotes, utils.utils as utils
from localdata import serverId, leerkrachtRoleId
from discord import Interaction, Member, app_commands
from discord.ext import commands
from utils.utils import isStaff
from modules.roleManager.roleManager import *

class roleManagerCog(commands.Cog):
    def __init__(self, bot):
        self.bot : discord.Client = bot
        self.rolesPendingRemoval = getRolesPendingRemoval()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Role Manager Cog is ready")

        queue = queuePendingRemovals(self.bot.get_guild(serverId), self.rolesPendingRemoval)
        if len(queue) > 0: await asyncio.gather(*queue, return_exceptions=True)

    @app_commands.command(name="giveleerkrachtrole", description="Geef de leerkracht rol aan iemand")
    @app_commands.describe(user="username", duration="duration in minutes")
    @utils.catcherrors
    async def giveleerkrachtrole(self, i9n: Interaction, user: Member, duration: int = 180) -> None:
        assert isStaff(i9n.user), quotes.NOT_STAFF_ERROR
        await giveTemporaryRole(self.rolesPendingRemoval, i9n, user, i9n.guild.get_role(leerkrachtRoleId), duration)

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