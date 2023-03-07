from discord.ext import commands
from discord.ext.commands import CommandError
from discord import ForumChannel, app_commands
import discord
from data import kelderID, tagAnsweredID
from localdata import serverID
import utils.utils as utils

class channelManagerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Channel Manager Cog is ready")

    @app_commands.command(
        name="beanwoord", 
        description="Mark forum post as answered.")
    @utils.catcherrors
    async def beantwoord(self, interaction):
        if not isinstance(interaction.channel.parent, ForumChannel): raise CommandError("Not in forum")

        answeredTag = interaction.channel.parent.get_tag(tagAnsweredID)

        isOwner = interaction.channel.owner == interaction.message.author
        isStaff = utils.isStaff(interaction.message.author)

        if not (isOwner or isStaff): raise CommandError("You must be the owner of the post or a staff member")
        if answeredTag in interaction.channel.applied_tags: raise CommandError("Thread already marked as answered")
        
        await interaction.channel.add_tags(answeredTag)
        await interaction.response.send_message("Thread marked as answered")
    
    @commands.command(
        description="Get IDs of tags in forum. Staff only.")
    @utils.catcherrors
    async def debug_gettagids(self, ctx):
        if not utils.isStaff(ctx.message.author): raise CommandError("This command is staff-only.")
        if not isinstance(ctx.channel.parent, ForumChannel): raise CommandError("Not in forum")
        for tag in ctx.channel.parent.available_tags: await ctx.send(f"{tag.id} - {tag.emoji}")

    @app_commands.command(name="limiet",
        description="Sets the user limit of #kelder VC")
    @utils.catcherrors
    async def limiet(self, interaction, limiet: int):
        channel = self.bot.get_channel(kelderID)
    
        if not (interaction.user in channel.members): raise CommandError("Je zit niet in #kelder")
        if limiet < 3 or limiet > 8: raise CommandError("De limiet moet tussen 3 en 8 liggen.")
    
        await channel.edit(user_limit = limiet)
        await interaction.response.send_message(f"De limiet is nu {limiet}.")

async def setup(bot):
    await bot.add_cog(channelManagerCog(bot), guild = discord.Object(id = serverID))