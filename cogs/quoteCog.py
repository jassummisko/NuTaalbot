import discord, \
    data.botResponses as botResponses, \
    utils.genUtils as genUtils
from modules.quotes.quotes import *
from discord.ext import commands
from data.localdata import serverId
from discord.ext.commands import CommandError
from discord import app_commands

AssertionError = CommandError

class quoteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Quote Cog is ready")

    @app_commands.command(name='quote', description='Invoke a quote')
    @app_commands.describe(label='Label of quote')
    @genUtils.catcherrors
    async def quote(self, i9n: discord.Interaction, label: str):
        quote = getQuote(label)
        await i9n.response.send_message(f"`id: {quote['id']}`: {quote['txt']}")

    @app_commands.command(name='removequote', description='Remove a quote')
    @app_commands.describe(id='ID of the quote')
    @genUtils.catcherrors
    async def removequote(self, i9n: discord.Interaction, id: str):
        removeQuote(id)
        await i9n.response.send_message(f"Removed quote with id '{id}'.")

    @app_commands.command(name='addquote', description='Add a quote')
    @app_commands.describe(label='Label of the quote', quote="The quote itself.")
    @genUtils.catcherrors
    async def addquote(self, i9n: discord.Interaction, label: str, quote: str):
        addQuote(i9n.user, label, quote)
        await i9n.response.send_message(f"Added: '{quote}' with label '{label}'")

async def setup(bot):
    await bot.add_cog(quoteCog(bot), guilds = [discord.Object(id = serverId)])