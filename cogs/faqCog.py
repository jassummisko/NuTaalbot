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
        print("FAQ Cog is ready") 
        if checkToBeUpdated(forceUpdate=False):
            getFaqsFromWiki()
            print("FAQ Updated")
        else:
            print("FAQ in no need of update")

    @commands.command()
    @tryexcept
    async def updateFaqs(self, ctx):
        if not isStaff(ctx.author):
            await ctx.send("You have no permissions to use this command.")
            return
        await ctx.send("Updating FAQs...")
        getFaqsFromWiki()
        await ctx.send("FAQs Updated")

    @commands.command(aliases=["faq_list"])
    @tryexcept
    async def faqlist(self, ctx):
        message = "**__Here is a list of all FAQ's:__**\n"
        for alias in getListOfFaqAliases():
            name, description = alias
            message += f"**{name}** - {description}\n"
        message += "\nTo start an FAQ, type `!faq` followed by the name: ex. `!faq heelveel`"

        await ctx.send(message)

    @commands.command()
    @tryexcept
    async def faq(self, ctx):
        bot = self.bot
        label = " ".join(ctx.message.content.split()[1:])

        if label == '':
            await ctx.send("Gebruik: !faq <FAQ_NAAM>")
            return
        
        faq = FAQ(label)
        while True:
            await ctx.send(faq.getMessage())
            if faq.isEnd: break

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