import discord, data.botResponses as botResponses
from discord.ext import commands
from discord.ext.commands import CommandError
from discord import ForumChannel, app_commands
from data.dataIds import kelderId, tagAnsweredId
from data.localdata import serverId
from utils import genUtils

AssertionError = CommandError

class channelManagerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Channel Manager Cog is ready")

    @app_commands.command(
        name="beantwoord", 
        description="Mark forum post as answered.")
    @genUtils.catcherrors
    async def beantwoord(self, i9n: discord.Interaction):
        assert isinstance(i9n.channel, discord.Thread)
        assert isinstance(i9n.channel.parent, ForumChannel), botResponses.NOT_IN_FORUM_ERROR

        assert isinstance(user := i9n.user, discord.Member)
        isOwnerOrStaff = (i9n.channel.owner == i9n.user) or genUtils.isStaff(user)
        assert isOwnerOrStaff, botResponses.NOT_POST_OWNER_OR_STAFF_ERROR

        assert (answeredTag := i9n.channel.parent.get_tag(tagAnsweredId))
        assert answeredTag not in i9n.channel.applied_tags, botResponses.THREAD_ANSWERED

        await i9n.channel.add_tags(answeredTag)
        await i9n.response.send_message(botResponses.THREAD_ANSWERED)

    @app_commands.command(name="limiet",
        description="Sets the user limit of #kelder VC")
    @genUtils.catcherrors
    async def limiet(self, i9n: discord.Interaction, limit: int):
        channel = self.bot.get_channel(kelderId)
        assert (i9n.user in channel.members), botResponses.NOT_IN_KELDER_ERROR

        LOWER_LIMIT, UPPER_LIMIT = 3, 8
        assert (LOWER_LIMIT <= limit <= UPPER_LIMIT), botResponses.KELDER_LIMIET_ERROR
    
        await channel.edit(user_limit = limit)
        await i9n.response.send_message(botResponses.KELDER_LIMIER_UPDATED.format(limit))

async def setup(bot: commands.Bot):
    await bot.add_cog(channelManagerCog(bot), guilds=[discord.Object(id = serverId)])
