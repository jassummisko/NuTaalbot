from discord.ext import commands
import discord
from discord import app_commands
import asyncio
from modules.faq.faq import *
from localdata import serverID
from utils.utils import isStaff
import utils.utils as utils
import data.quotes as quotes
from discord.ext.commands import CommandError

AssertionError = CommandError

class faqCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Checking if FAQ is to be updated...")
        if checkToBeUpdated(forceUpdate=False):
            print("Updating FAQ...")
            getFaqsFromWiki()
            print("FAQ Updated")
        else: print("FAQ in no need of update")
        print("FAQ Cog is ready")

    @app_commands.command(name="updatefaqs", description="FAQ updaten.")
    @utils.catcherrors
    async def updatefaqs(self, i9n: discord.Interaction):
        assert isStaff(i9n.user), quotes.NOT_STAFF_ERROR
        await i9n.response.send_message(quotes.UPDATING_FAQ)
        getFaqsFromWiki()
        msg = await i9n.original_response()
        await msg.edit(content=quotes.FAQ_UPDATED)

    @app_commands.command(name="faqlist", description="Lists all available FAQs.")
    @utils.catcherrors
    async def faqlist(self, i9n):
        message = "**__Here is a list of all FAQ's:__**\n"
        for alias in getListOfFaqAliases():
            name, description = alias
            message += f"**{name}** - {description}\n"
        message += "\nTo start an FAQ, type `!faq` followed by the name: ex. `!faq heelveel`"

        await i9n.response.send_message(message)

    @app_commands.command(name="faq", description="Calls an FAQ.")
    @app_commands.describe(label="Name of FAQ.")
    @utils.catcherrors
    async def faq(self, i9n, label: str):
        bot = self.bot
        ctx = await bot.get_context(i9n)
        await i9n.response.send_message(quotes.RUNNING_FAQ.format(label))
        faq = FAQ(label)
        while True:
            await ctx.send(faq.getMessage())
            if faq.isEnd: 
                await ctx.send(quotes.FAQ_ENDED)
                break

            def check(m):
                isSameUser = m.author == ctx.author
                isSameChannel = m.channel == ctx.channel
                return isSameUser and isSameChannel

            try: msg = await bot.wait_for("message", timeout=120, check=check)
            except asyncio.TimeoutError:
                await ctx.send(quotes.TIMED_OUT)
                return

            faq.check(msg)

    @app_commands.command(name="registerfaq", description="FAQ registreren.")
    @app_commands.describe(name="Naam van faq", label="Beginlabel van faq", desc="Beschrijving van faq")
    @utils.catcherrors
    async def registerfaq(self, i9n, name: str, label: str, desc: str):
        assert isStaff(i9n.user), quotes.NOT_STAFF_ERROR

        addFaqAlias(name, label, desc)
        await i9n.response.send_message(quotes.FAQ_REGISTERED.format(name, label))

    @app_commands.command(name="deregisterfaq", description="FAQ verwijderen van register.")
    @app_commands.describe(name="Naam van faq")
    @utils.catcherrors
    async def deregisterfaq(self, i9n, name: str):
        assert isStaff(i9n.user), quotes.NOT_STAFF_ERROR
        assert removeFaqAlias(name), quotes.NOT_FAQ_ERROR.format(name) 
        await i9n.response.send_message(quotes.FAQ_DEREGISTERED.format(name))
       
    @app_commands.command(name="debug_faq", description="Calls an unregistered FAQ from a label.")
    @app_commands.describe(label="Name of FAQ.")
    @utils.catcherrors
    async def debug_faq(self, i9n, label: str): 
        assert isStaff(ctx.author), quotes.NOT_STAFF_ERROR

        ctx = await self.bot.get_context(i9n)
        faq = FAQ(label, debug=True)
        while True:
            await ctx.send(faq.getMessage())
            if faq.isEnd: 
                await ctx.send(quotes.FAQ_ENDED)
                break

            def check(m):
                isSameUser = m.author == ctx.author
                isSameChannel = m.channel == ctx.channel
                return isSameUser and isSameChannel

            try: msg = await self.bot.wait_for("message", timeout=120, check=check)
            except asyncio.TimeoutError:
                await ctx.send(quotes.TIMED_OUT)
                return

            faq.check(msg)

async def setup(bot):
    await bot.add_cog(faqCog(bot), guild = discord.Object(id = serverID))