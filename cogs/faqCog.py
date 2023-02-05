from discord.ext import commands
import asyncio
from faq import FAQ
import yaml

class faqCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("FAQ Cog is ready")

    @commands.command()
    async def faqlist(self, ctx):
        with open("faqdata/faqaliases.yaml") as file:
            aliases = yaml.load(file, Loader=yaml.Loader)
        allAliases = sorted(aliases.keys())
        message = "**__Here is a list of all FAQ's:__**\n"
        for alias in allAliases:
            print(alias)
            message += f"**{alias}** - {aliases[alias]['description']}\n"
        message += "\nTo start an FAQ, type `!faq` followed by the name: ex. `!faq heelveel`"
        await ctx.send(message)

    @commands.command()
    async def faq(self, ctx):
        bot = self.bot
        label = " ".join(ctx.message.content.split()[1:])

        faq = FAQ(label)

        while True:
            await ctx.send(faq.getMessage())

            if not faq.isContinue: break
            try:
                msg = await bot.wait_for("message", timeout=120)
            except asyncio.TimeoutError:
                await ctx.send("Timed out!")
                return

            faq.check(msg)
            
async def setup(bot):
    await bot.add_cog(faqCog(bot))