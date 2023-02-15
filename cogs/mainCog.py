from discord.ext import commands
from data import kelderID
import modules.beginners.beginners as beginners
from utils import tryexcept

class mainCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Main Cog is ready")

    @tryexcept
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Gebruik: {ctx.prefix}{ctx.command.name} {ctx.command.signature}")
            if ctx.command.name == "faq": await ctx.send("Met `!faqlist` zie je alle faqs.")

    @commands.command(description="Says hi to the bot!")
    @tryexcept
    async def hi(self, ctx):
        await ctx.send("Elk zinnen dah!")

    @commands.command(aliases=["🦵"], description="Checks if a word is B1 using ishetb1.nl.")
    @tryexcept
    async def b1(self, ctx, woord):
        message = beginners.ScrapeB1(woord)
        await ctx.send(message)

    @commands.command(description="Sets the user limit of #kelder VC")
    @tryexcept
    async def limiet(self, ctx, limiet):
        channel = self.bot.get_channel(824353793915224125)
        member = ctx.author

        if not (member in channel.members):
            await ctx.send("Je zit niet in #kelder.")
            return

        newLimit = int(limiet)
        if newLimit < 3 or newLimit > 8:
            await ctx.send("De limiet moet tussen 3 en 8 liggen.")
            return
        
        await channel.edit(user_limit = newLimit)
        await ctx.send(f"De limiet is nu {newLimit}.")

    @commands.command(aliases=["help"], description="Lists all bot commands.")
    @tryexcept
    async def hulp(self, ctx):
        helptext = ""
        commands = sorted([command for command in self.bot.commands], key=lambda x: x.name)
        for command in commands: helptext += f"**{command}** -- {command.description}\n"
        await ctx.send(helptext)

async def setup(bot):
    await bot.add_cog(mainCog(bot))