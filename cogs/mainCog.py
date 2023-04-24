import discord, \
    data.botResponses as botResponses
from discord.ext import commands
from data.localdata import serverId
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
        await ctx.send(botResponses.ELK_ZINNEN_DAH)

async def setup(bot):
    await bot.add_cog(mainCog(bot), guilds = [discord.Object(id = serverId)])
