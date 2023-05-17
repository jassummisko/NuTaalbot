import discord, asyncio, \
    utils.genUtils as genUtils, \
    data.botResponses as botResponses
from discord.ext import commands
from discord import app_commands
from modules.faq.faq import *
from data.localdata import serverId
from utils.genUtils import isStaff
from discord.ext.commands import CommandError
from discord.app_commands import Choice
from fuzzywuzzy import fuzz 

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
    @genUtils.catcherrors
    async def updatefaqs(self, i9n: discord.Interaction):
        assert isinstance(i9n.user, discord.Member)
        if not isStaff(i9n.user): raise CommandError(botResponses.NOT_STAFF_ERROR)
        await i9n.response.send_message(botResponses.UPDATING_FAQ)
        getFaqsFromWiki()
        msg = await i9n.original_response()
        await msg.edit(content=botResponses.FAQ_UPDATED)

    @app_commands.command(name="faqlist", description="Lists all available FAQs.")
    @genUtils.catcherrors
    async def faqlist(self, i9n: discord.Interaction):
        message = "**__Here is a list of all FAQ's:__**\n"
        for alias in getListOfFaqAliases():
            name, description = alias
            message += f"**{name}** - {description}\n"
        message += "\nTo start an FAQ, type `!faq` followed by the name: ex. `!faq heelveel`"
        await i9n.response.send_message(message)

    @app_commands.command(name="faq", description="Calls an FAQ.")
    @app_commands.describe(label="Name of FAQ.")
    @genUtils.catcherrors
    async def faq(self, i9n: discord.Interaction, label: str):
        bot = self.bot
        ctx = await bot.get_context(i9n)
        await i9n.response.send_message(botResponses.RUNNING_FAQ.format(label))
        faq = FAQ(label)
        while True:
            await i9n.response.edit_message(content=faq.getMessage())
            if faq.isEnd: 
                await ctx.send(botResponses.FAQ_ENDED)
                break

            def check(m):
                isSameUser = m.author == ctx.author
                isSameChannel = m.channel == ctx.channel
                return isSameUser and isSameChannel

            try: msg = await bot.wait_for("message", timeout=120, check=check)
            except asyncio.TimeoutError: 
                await ctx.send("Timed out!")
                break
            else: faq.check(msg)

    @faq.autocomplete('label')
    async def faq_autocomplete(self, _: discord.Interaction, current: str):
        registeredFaqs = [f[0] for f in getListOfFaqAliases()]
        registeredFaqs = sorted(registeredFaqs, key=(lambda role: fuzz.ratio(role.lower(), current.lower())), reverse=True)
        amountOfSuggestions = min(len(registeredFaqs), 10)
        return [Choice(name=faqname, value=faqname) for faqname in registeredFaqs[:amountOfSuggestions]] 
    
    @app_commands.command(name="registerfaq", description="FAQ registreren.")
    @app_commands.describe(naam="Naam van faq", label="Beginlabel van faq", beschrijving="Beschrijving van faq")
    @genUtils.catcherrors
    async def registerfaq(self, i9n, naam: str, label: str, beschrijving: str):
        if not isStaff(i9n.user): raise CommandError(botResponses.NOT_STAFF_ERROR)
        addFaqAlias(naam, label, beschrijving)
        await i9n.response.send_message(f"FAQ '{naam}' is geregistreerd met label '{label}' als begin.")

    @app_commands.command(name="deregisterfaq", description="FAQ verwijderen van register.")
    @app_commands.describe(name="Naam van faq")
    @genUtils.catcherrors
    async def deregisterfaq(self, i9n: discord.Interaction, name: str):
        assert isinstance(i9n.user, discord.Member)
        if not isStaff(i9n.user): raise CommandError(botResponses.NOT_STAFF_ERROR)
        if not removeFaqAlias(name): CommandError(botResponses.NOT_FAQ_ERROR.format(name))
        await i9n.response.send_message(botResponses.FAQ_DEREGISTERED.format(name))
       
    @app_commands.command(name="debug_faq", description="Calls an unregistered FAQ from a label.")
    @app_commands.describe(label="Name of FAQ.")
    @genUtils.catcherrors
    async def debug_faq(self, i9n: discord.Interaction, label: str): 
        assert isinstance(i9n.user, discord.Member)
        if not isStaff(ctx.message.author): raise CommandError(botResponses.NOT_STAFF_ERROR)
        ctx = await self.bot.get_context(i9n)
        faq = FAQ(label, debug=True)
        while True:
            await ctx.send(faq.getMessage())
            if faq.isEnd: 
                await ctx.send(botResponses.FAQ_ENDED)
                break

            def check(m):
                isSameUser = m.author == ctx.author
                isSameChannel = m.channel == ctx.channel
                return isSameUser and isSameChannel

            try: msg = await self.bot.wait_for("message", timeout=120, check=check)
            except asyncio.TimeoutError: await ctx.send("Timed out!")
            else: faq.check(msg)

async def setup(bot: commands.Bot):
    await bot.add_cog(faqCog(bot), guild = discord.Object(id = serverId))