from discord.ext import commands
import datetime as dt
from utils import tryexcept

channelID = 1071803725343101048
roleID = 837470147404496898

class channelCheckerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tryexcept
    @commands.Cog.listener()
    async def on_ready(self):
        print("Channel Checker Cog is ready")

        channel = self.bot.get_channel(channelID)
        role = channel.guild.get_role(roleID)
        today = dt.datetime.now(dt.timezone.utc)

        def getHistory(): 
            return channel.history(limit=None, after=today - dt.timedelta(days=60))

        users = set([msg.author async for msg in getHistory()])

        for user in set(role.members).difference(users): 
            await user.remove_roles(role)

        warnedUsers = []
        async for message in getHistory():
            user = message.author

            if (today - message.created_at).days != 30: continue
            if user not in role.members or user in warnedUsers: continue

            await user.send("U r dum")
            warnedUsers.append(user)
        
async def setup(bot):
    await bot.add_cog(channelCheckerCog(bot))
