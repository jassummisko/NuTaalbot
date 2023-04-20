import discord, \
    data.botResponses as botResponses, \
    utils.genUtils as genUtils 
from discord.ext import commands
from data.localdata import serverId
from discord.ext.commands import CommandError

AssertionError = CommandError

class quoteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Quote Cog is ready")

    

async def setup(bot):
    await bot.add_cog(quoteCog(bot), guilds = [discord.Object(id = serverId)])