from discord.ext import commands
import modules.beginners.beginners as beginners

class mainCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Main Cog is ready")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        message = ''
        if isinstance(error, commands.MissingRequiredArgument):
            message += f"Gebruik: `{ctx.prefix}{ctx.command.name} {ctx.command.signature}`"
            if ctx.command.name == "faq": message += "\nMet `!faqlist` zie je alle faqs."
            await ctx.send(message)

    @commands.command(description="Says hi to the bot!")
    async def hi(self, ctx):
        await ctx.send("Elk zinnen dah!")

    @commands.command(aliases=["🦵"], description="Checks if a word is B1 using ishetb1.nl.")
    async def b1(self, ctx, woord):
        message = beginners.ScrapeB1(woord)
        await ctx.send(message)

    @commands.command(aliases=["help"], description="Lists all bot commands.")
    async def hulp(self, ctx):
        commands = [
            f"**{command}** -- {command.description}" 
                for command in self.bot.commands
                if not "debug_" in command.name
        ]       + ["**stopfaq** -- Stop currently running faq."]
        commands = sorted(commands)

        await ctx.send(
            "__Here is a list of all bot commands:__\n"
            + "\n".join(commands)
        )

async def setup(bot):
    await bot.add_cog(mainCog(bot))