import discord, data.botResponses as botResponses
from discord.ext import commands
from discord.ext.commands import CommandError
from discord import ForumChannel, app_commands
from data.dataIds import kelderId, tagAnsweredId
from data.localdata import serverId
from utils import genUtils

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
        if not hasattr(i9n.channel, "parent"): raise CommandError(botResponses.NOT_IN_FORUM_ERROR)
        if not isinstance(i9n.channel.parent, ForumChannel): raise CommandError(botResponses.NOT_IN_FORUM_ERROR)

        isOwnerOrStaff = (i9n.channel.owner == i9n.user) or genUtils.isStaff(i9n.user)
        if not isOwnerOrStaff: raise CommandError(botResponses.NOT_POST_OWNER_OR_STAFF_ERROR)

        answeredTag = i9n.channel.parent.get_tag(tagAnsweredId)
        if answeredTag in i9n.channel.applied_tags: raise CommandError(botResponses.THREAD_ALREADY_ANSWERED)

        await i9n.channel.add_tags(answeredTag)
        await i9n.response.send_message(botResponses.THREAD_ANSWERED)

    @commands.command(
        description="Get IDs of tags in forum. Staff only.")
    @genUtils.catcherrors
    async def debug_gettagids(self, ctx: commands.Context):
        if not genUtils.isStaff(ctx.message.author): CommandError(botResponses.NOT_STAFF_ERROR)
        if not isinstance(ctx.channel.parent, ForumChannel): CommandError(botResponses.NOT_IN_FORUM_ERROR)
        for tag in ctx.channel.parent.available_tags: await ctx.send(f"{tag.id} - {tag.emoji}")

    @app_commands.command(name="limiet",
        description="Sets the user limit of #kelder VC")
    @genUtils.catcherrors
    async def limiet(self, i9n: discord.Interaction, limit: int):
        channel = self.bot.get_channel(kelderId)
        if not (i9n.user in channel.members): CommandError(botResponses.NOT_IN_KELDER_ERROR)

        LOWER_LIMIT, UPPER_LIMIT = 3, 8
        if not (LOWER_LIMIT <= limit <= UPPER_LIMIT): CommandError(botResponses.KELDER_LIMIET_ERROR)
    
        await channel.edit(user_limit = limit)
        await i9n.response.send_message(botResponses.KELDER_LIMIER_UPDATED.format(limit))

async def setup(bot: discord.Client):
    await bot.add_cog(channelManagerCog(bot), guilds=[discord.Object(id = serverId)])
