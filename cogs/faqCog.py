from discord.ext import commands
import discord
from discord import app_commands
import asyncio
from modules.faq.faq import *
<<<<<<< HEAD
from localdata import serverID
from utils import isStaff
=======
from utils.utils import isStaff
>>>>>>> a7a6a74d0af620296cc79194623e348e027b0d09

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
    async def updatefaqs(self, interaction):
        if not isStaff(interaction.user):
            await interaction.response.send_message("You have no permissions to use this command.")
            return
        await interaction.response.send_message("Updating FAQs...")
        getFaqsFromWiki()
        await interaction.response.send_message("FAQs Updated")

    @app_commands.command(name="faqlist", description="Lists all available FAQs.")
    async def faqlist(self, interaction):
        message = "**__Here is a list of all FAQ's:__**\n"
        for alias in getListOfFaqAliases():
            name, description = alias
            message += f"**{name}** - {description}\n"
        message += "\nTo start an FAQ, type `!faq` followed by the name: ex. `!faq heelveel`"

        await interaction.response.send_message(message)

    @commands.command(description="Starts specific FAQ.")
    async def faq(self, ctx, label):
        bot = self.bot
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
    async def registerfaq(self, interaction, naam: str, label: str, beschrijving: str):
        if not isStaff(interaction.user):
            await interaction.response.send_message("You must be a staff member to use this command.")
            return

        addFaqAlias(naam, label, beschrijving)
        await interaction.response.send_message(f"FAQ '{naam}' is geregistreerd met label '{label}' als begin.")

    @app_commands.command(name="deregisterfaq", description="FAQ verwijderen van register.")
    @app_commands.describe(naam="Naam van faq")
    async def deregisterfaq(self, interaction, naam: str):
        if not isStaff(interaction.user):
            await interaction.response.send_message("Je mag dit commando niet gebruiken omdat je geen staff bent.")
            return

        if not removeFaqAlias(naam):
            await interaction.response.send_message(f"Er zit geen FAQ met de '{naam}' in de lijst.")            
            return
        
        await interaction.response.send_message(f"FAQ '{naam}' verwijderd.")
       
    @commands.command(debug=True)
    async def debug_faq(self, ctx, label):
        if not isStaff(ctx.author):
            await ctx.send("You must be a staff member to use this command.")
            return

        bot = self.bot
        
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