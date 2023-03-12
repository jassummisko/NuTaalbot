import discord, pickle, os, asyncio
from localdata import serverID
from discord import Interaction, Role, Member
from discord.ext import commands
from discord import app_commands
from dataclasses import dataclass
import utils.utils as utils
import data.quotes as quotes
from utils.utils import isStaff
import datetime as dt

channelID = 1071803725343101048
roleID = 837470147404496898
filepath = "data/rolesPendingRemoval.pkl"

@dataclass
class PendingEntry:
    userId: int
    roleId: int
    time: dt.datetime

class roleManagerCog(commands.Cog):
    def __init__(self, bot):
        self.bot : discord.Client = bot
        self.guild = self.bot.get_guild(serverID)
        self.rolesPendingRemoval = []

    @commands.Cog.listener()
    async def on_ready(self):
        print("Role Manager Cog is ready")

        if os.path.isfile(filepath) and os.path.getsize(filepath) > 0:
            with open(filepath, 'r+b') as f:
                self.rolesPendingRemoval = pickle.load(f)

        async def removeRole(pendingEntry: PendingEntry):
            duration: dt.timedelta = dt.datetime.now() - pendingEntry.time
            await asyncio.sleep(duration.seconds)
            user = self.guild.get_member(pendingEntry.userId)
            role = self.guild.get_role(pendingEntry.roleId)
            user.remove_roles(role)

        for pendingEntry in self.rolesPendingRemoval:
            await removeRole(pendingEntry)



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

    @app_commands.command(name="giveleerkrachtrole", description="Geef de leerkracht rol aan iemand")
    @app_commands.describe(user="username", role="role name", duration="duration in minutes")
    @utils.catcherrors
    async def giveleerkrachtrole(self, i9n: Interaction, user : Member, role : Role, duration : int = 180) -> None:
        await self.giverole(i9n, user, role, duration)

    async def giverole(self, i9n: Interaction, user : Member, role : Role, duration : int) -> None:
        # assert isStaff(i9n.user), quotes.NOT_STAFF_ERROR
        SECONDS_PER_MINUTE : int = 60
        await user.add_roles(role)
        await i9n.response.send_message(quotes.ROLE_GIVEN.format(role.name))
        msg = await i9n.original_response()
        t = dt.datetime.now() + dt.timedelta(duration)
        self.rolesPendingRemoval.append(PendingEntry(user.id, role.id, t))
        with open(filepath, 'w+b') as f:
            pickle.dump(self.rolesPendingRemoval, f)
        await asyncio.sleep(duration*SECONDS_PER_MINUTE)
        await user.remove_roles(role)
        await user.send(content=quotes.ROLE_REMOVED.format(role.name))

async def setup(bot):
    await bot.add_cog(roleManagerCog(bot), guilds=[discord.Object(id=serverID)])
