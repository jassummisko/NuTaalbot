from discord.ext import commands
from discord.ext.commands import CommandError
from discord import ForumChannel, app_commands
import discord
from dataIds import kelderId, tagAnsweredId
from localdata import serverId
from utils import genUtils
import data.quotes as quotes

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
        assert hasattr(i9n.channel, "parent"), quotes.NOT_IN_FORUM_ERROR
        assert isinstance(i9n.channel.parent, ForumChannel), quotes.NOT_IN_FORUM_ERROR

        isOwnerOrStaff = (i9n.channel.owner == i9n.user) or genUtils.isStaff(i9n.user)
        assert isOwnerOrStaff, quotes.NOT_POST_OWNER_OR_STAFF_ERROR

        answeredTag = i9n.channel.parent.get_tag(tagAnsweredId)
        assert answeredTag not in i9n.channel.applied_tags, quotes.THREAD_ANSWERED

        await i9n.channel.add_tags(answeredTag)
        await i9n.response.send_message(quotes.THREAD_ANSWERED)

    @commands.command(
        description="Get IDs of tags in forum. Staff only.")
    @genUtils.catcherrors
    async def debug_gettagids(self, ctx):
        assert genUtils.isStaff(ctx.message.author), quotes.NOT_STAFF_ERROR
        assert isinstance(ctx.channel.parent, ForumChannel), quotes.NOT_IN_FORUM_ERROR
        for tag in ctx.channel.parent.available_tags: await ctx.send(f"{tag.id} - {tag.emoji}")

    @app_commands.command(name="limiet",
        description="Sets the user limit of #kelder VC")
    @genUtils.catcherrors
    async def limiet(self, i9n: discord.Interaction, limit: int):
        channel = self.bot.get_channel(kelderId)
        assert (i9n.user in channel.members), quotes.NOT_IN_KELDER_ERROR

        LOWER_LIMIT, UPPER_LIMIT = 3, 8
        assert (LOWER_LIMIT <= limit <= UPPER_LIMIT), quotes.KELDER_LIMIET_ERROR
    
        await channel.edit(user_limit = limit)
        await i9n.response.send_message(quotes.KELDER_LIMIER_UPDATED.format(limit))

async def setup(bot):
    await bot.add_cog(channelManagerCog(bot), guilds=[discord.Object(id = serverId)])
