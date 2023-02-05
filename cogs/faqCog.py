from discord.ext import commands
import asyncio
from faq import FAQ

class faqCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("FAQ Cog is ready")

    @commands.command()
    async def faq(self, ctx):
        bot = self.bot
        label = " ".join(ctx.message.content.split()[1:])
        faq = FAQ(label)

        while True:
            await ctx.send(faq.getMessage())

            if not faq.isContinue: break
            try:
                msg = await bot.wait_for("message", timeout=60)
            except asyncio.TimeoutError:
                await ctx.send("Timed out!")
                return

            faq.check(msg)
            
async def setup(bot):
    await bot.add_cog(faqCog(bot))