from discord.ext import commands
from discord import ForumChannel
from data import kelderID, tagAnsweredID
import utils

class channelManagerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Channel Manager Cog is ready")

    @commands.command(
        aliases=["answered"], 
        description="Mark forum post as answered.")
    async def beantwoord(self, ctx):
        if not isinstance(ctx.channel.parent, ForumChannel):
            await ctx.send("Not in forum")
            return

        answeredTag = ctx.channel.parent.get_tag(tagAnsweredID)

        isOwner = ctx.channel.owner == ctx.message.author
        isStaff = utils.isStaff(ctx.message.author)

        if not (isOwner or isStaff):
            await ctx.send("You must be the owner of the post or a staff member")
            return

        if answeredTag in ctx.channel.applied_tags:
            await ctx.send("Thread already marked as answered")
            return
        
        await ctx.channel.add_tags(answeredTag)
        await ctx.send("Thread marked as answered")
    
    @commands.command(
        description="Get IDs of tags in forum. Staff only.")
    async def debug_gettagids(self, ctx):
        if not utils.isStaff(ctx.message.author):
            await ctx.send("This command is staff-only.")
            return

        if not isinstance(ctx.channel.parent, ForumChannel):
            await ctx.send("Not in forum")
            return

        for tag in ctx.channel.parent.available_tags:
            await ctx.send(f"{tag.id} - {tag.emoji}")

    @commands.command(
        description="Sets the user limit of #kelder VC")
    async def limiet(self, ctx, limiet):
        channel = self.bot.get_channel(kelderID)
        member = ctx.author

        if not (member in channel.members):
            await ctx.send("Je zit niet in #kelder.")
            return

        newLimit = int(limiet)
        if newLimit < 3 or newLimit > 8:
            await ctx.send("De limiet moet tussen 3 en 8 liggen.")
            return
        
        await channel.edit(user_limit = newLimit)
        await ctx.send(f"De limiet is nu {newLimit}.")

async def setup(bot):
    await bot.add_cog(channelManagerCog(bot))