from discord.ext import commands
import discord
from discord import app_commands
import asyncio
from modules.faq.faq import *
from localdata import serverID
from utils.utils import isStaff
import utils.utils as utils
from discord.ext.commands import CommandError

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
        else:
            print("FAQ in no need of update")
        print("FAQ Cog is ready")

    @app_commands.command(name="updatefaqs", description="FAQ updaten.")
    @utils.catcherrors
    async def updatefaqs(self, interaction):
        if not isStaff(interaction.user):
            await interaction.response.send_message("You have no permissions to use this command.")
            return
        await interaction.response.send_message("Updating FAQs...")
        getFaqsFromWiki()
        await interaction.response.send_message("FAQs Updated")

    @app_commands.command(name="faqlist", description="Lists all available FAQs.")
    @utils.catcherrors
    async def faqlist(self, interaction):
        message = "**__Here is a list of all FAQ's:__**\n"
        for alias in getListOfFaqAliases():
            name, description = alias
            message += f"**{name}** - {description}\n"
        message += "\nTo start an FAQ, type `!faq` followed by the name: ex. `!faq heelveel`"

        await interaction.response.send_message(message)

    @app_commands.command(name="faq", description="Calls an FAQ.")
    @app_commands.describe(label="Name of FAQ.")
    @utils.catcherrors
    async def faq(self, interaction, label: str):
        bot = self.bot
        ctx = await bot.get_context(interaction)
        await interaction.response.send_message(f"Running FAQ {label}")
        faq = FAQ(label)
        while True:
            await ctx.send(faq.getMessage())
            if faq.isEnd: 
                await ctx.send("FAQ ended.")
                break

            def check(m):
                isSameUser = m.author == ctx.author
                isSameChannel = m.channel == ctx.channel
                return isSameUser and isSameChannel

            try: msg = await bot.wait_for("message", timeout=120, check=check)
            except asyncio.TimeoutError:
                await ctx.send("Timed out!")
                return

            faq.check(msg)
    
    @app_commands.command(name="registerfaq", description="FAQ registreren.")
    @app_commands.describe(naam="Naam van faq", label="Beginlabel van faq", beschrijving="Beschrijving van faq")
    @utils.catcherrors
    async def registerfaq(self, interaction, naam: str, label: str, beschrijving: str):
        if not isStaff(interaction.user): raise CommandError("You must be a staff member to use this command.")

        addFaqAlias(naam, label, beschrijving)
        await interaction.response.send_message(f"FAQ '{naam}' is geregistreerd met label '{label}' als begin.")

    @app_commands.command(name="deregisterfaq", description="FAQ verwijderen van register.")
    @app_commands.describe(naam="Naam van faq")
    @utils.catcherrors
    async def deregisterfaq(self, interaction, naam: str):
        if not isStaff(interaction.user): raise CommandError("Je mag dit commando niet gebruiken omdat je geen staff bent.") 
        if not removeFaqAlias(naam): raise CommandError(f"Er zit geen FAQ met de '{naam}' in de lijst.")            
        
        await interaction.response.send_message(f"FAQ '{naam}' verwijderd.")
       
    @app_commands.command(name="debug_faq", description="Calls an unregistered FAQ from a label.")
    @app_commands.describe(label="Name of FAQ.")
    @utils.catcherrors
    async def debug_faq(self, interaction, label: str): 
        if not isStaff(ctx.author): raise CommandError("You must be a staff member to use this command.")

        bot = self.bot
        ctx = await bot.get_context(interaction)
        faq = FAQ(label, debug=True)
        while True:
            await ctx.send(faq.getMessage())
            if faq.isEnd: 
                await ctx.send("FAQ ended.")
                break

            def check(m):
                isSameUser = m.author == ctx.author
                isSameChannel = m.channel == ctx.channel
                return isSameUser and isSameChannel

            try: msg = await bot.wait_for("message", timeout=120, check=check)
            except asyncio.TimeoutError:
                await ctx.send("Timed out!")
                return

            faq.check(msg)

async def setup(bot):
    await bot.add_cog(faqCog(bot), guild = discord.Object(id = serverID))