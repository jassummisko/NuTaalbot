from discord.ext import commands
import asyncio
from modules.faq.faq import *
from utils import tryexcept, isStaff

class faqCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tryexcept
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

    @commands.command(description="Updates list of faqs. Staff only.")
    @tryexcept
    async def updateFaqs(self, ctx):
        if not isStaff(ctx.author):
            await ctx.send("You have no permissions to use this command.")
            return
        await ctx.send("Updating FAQs...")
        getFaqsFromWiki()
        await ctx.send("FAQs Updated")

    @commands.command(aliases=["faq_list"], description="Lists all available FAQs.")
    @tryexcept
    async def faqlist(self, ctx):
        message = "**__Here is a list of all FAQ's:__**\n"
        for alias in getListOfFaqAliases():
            name, description = alias
            message += f"**{name}** - {description}\n"
        message += "\nTo start an FAQ, type `!faq` followed by the name: ex. `!faq heelveel`"

        await ctx.send(message)

    @commands.command(description="Starts specific FAQ.")
    @tryexcept
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
    
    @commands.command(description="Register an FAQ from the wiki. Staff only.")
    @tryexcept
    async def registerfaq(self, ctx, name, label, description):
        if not isStaff(ctx.author):
            ctx.send("You must be a staff member to use this command.")
            return

        addFaqAlias(name, label, description)

    @commands.command(debug=True)
    @tryexcept
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
    await bot.add_cog(faqCog(bot))