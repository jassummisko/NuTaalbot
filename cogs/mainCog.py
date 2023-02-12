from discord.ext import commands
from data import kelderID
import modules.beginners.beginners as beginners

class mainCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Main Cog is ready")

    @commands.command()
    async def hi(self, ctx):
        await ctx.send("Elk zinnen dah!")

    @commands.command(aliases=["🦵"])
    async def b1(self, ctx):
        args = ctx.message.content.split()
        if len(args) <= 1:
            await ctx.send("Gebruik: !b1 <WOORD>")
            return
        
        word = args[1]
        message = beginners.ScrapeB1(word)
        await ctx.send(message)

    @commands.command()
    async def limiet(self, ctx):
        args = ctx.message.content.split()
        if len(args) <= 1:
            await ctx.send("Gebruik: !limiet <WOORD>")
            return

        channel = self.bot.get_channel(kelderID)
        member = ctx.author

        if not (member in channel.members):
            await ctx.send("Je zit niet in #kelder.")
            return

        newLimit = int(args[1])
        if newLimit < 3 or newLimit > 8:
            await ctx.send("De limiet moet tussen 3 en 8 liggen.")
            return
        
        await channel.edit(user_limit = newLimit)
        await ctx.send(f"De limiet is nu {newLimit}.")

async def setup(bot):
    await bot.add_cog(mainCog(bot))
