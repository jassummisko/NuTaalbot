from discord.ext import commands
from discord import app_commands
import discord
from data.localdata import serverId
import data.quotes as quotes
import utils.genUtils as genUtils
import modules.beginners.beginners as beginners
from discord.ext.commands import CommandError

AssertionError = CommandError

class mainCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Main Cog is ready")

    @commands.command(description="Says hi to the bot!")
    async def hi(self, ctx: commands.Context):
        await ctx.send(quotes.ELK_ZINNEN_DAH)

    @app_commands.command(name="b1", description="Checks if a word a word is B1 using ishetb1.nl")
    @app_commands.describe(woord="Word to check.")
    @genUtils.catcherrors
    async def b1(self, i9n: discord.Interaction, woord: str):
        message = beginners.ScrapeB1(woord)
        await i9n.response.send_message(message)

async def setup(bot):
    await bot.add_cog(mainCog(bot), guilds = [discord.Object(id = serverId)])