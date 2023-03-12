from discord.ext import commands
from discord import app_commands
import discord
from localdata import serverID
import utils.utils as utils
import modules.beginners.beginners as beginners

### TEMPORARY ###
commandNames = [
    'faq',
    'faqlist',
    'b1',
    'beantwoord',
    'limiet'
] 

### TEMPORARY ###
commandNames = [
    'faq',
    'faqlist',
    'b1',
    'beantwoord',
    'limiet'
] 

class mainCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Main Cog is ready")

    @commands.Cog.listener()
    async def on_message(self, msg):
        if len(msg.content) <= 1: return
        cmd = msg.content.split()[0]
        if (cmd[0] == "!") and (cmd[1:] in commandNames):
            await msg.reply(content=f"We have migrated to slash commands. Please use `/{msg.content[1:]}` instead of `!{msg.content[1:]}`.")

    @commands.command(description="Says hi to the bot!")
    async def hi(self, ctx):
        await ctx.send("Elk zinnen dah!")

    @app_commands.command(name="b1", description="Checks if a word a word is B1 using ishetb1.nl")
    @app_commands.describe(woord="Word to check.")
    @utils.catcherrors
    async def b1(self, i9n, woord: str):
        message = beginners.ScrapeB1(woord)
        await i9n.response.send_message(message)

async def setup(bot):
    await bot.add_cog(mainCog(bot), guilds = [discord.Object(id = serverID)])