import discord, \
    data.quotes as quotes, \
    utils.genUtils as genUtils 
from discord.ext import commands
from discord import app_commands
from data.localdata import serverId
from modules.scraper.scraper import *
from modules.scraper.woordenlijst import *
from discord.ext.commands import CommandError

AssertionError = CommandError

class scraperCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Scraper Cog is ready")

    @app_commands.command(name="b1", description="Checks if a word a word is B1 using ishetb1.nl")
    @app_commands.describe(woord="Word to check.")
    @genUtils.catcherrors
    async def b1(self, i9n: discord.Interaction, woord: str):
        message = ScrapeB1(woord)
        await i9n.response.send_message(message)

    @app_commands.command(name="dehet", description="Is it de or het?")
    @app_commands.describe(woord="Word to check.")
    @genUtils.catcherrors
    async def dehet(self, i9n: discord.Interaction, woord: str):
        scraped: list[WordEntry] = checkWoordenlijst(woord)
        words: list[WordEntry] = []
        embed = discord.Embed(title=f"Resultaten voor \"{woord}\"")
        
        if not scraped: message = quotes.DEHET_NOWORD.format(woord)
        else: words: list[WordEntry] = [word for word in scraped if word.partOfSpeech == "znw"]
        
        if (not words) or len(words) == 0: message = quotes.DEHET_NONOUN.format(woord)
        elif len(words) == 1:
            message = quotes.DEHET_SINGLEWORD.format(words[0].grammaticalInfo['art'], words[0].lemma)
            embed.add_field(name = f"{words[0].grammaticalInfo['art']} {words[0].lemma}")
        elif len(words) > 1:
            message = ""
            for word in words:
                message += quotes.DEHET_MULTIWORD.format(
                    word.grammaticalInfo['art'],
                    word.lemma,
                    word.grammaticalInfo['gloss']
                )

        embed.description = message.strip()
        await i9n.response.send_message(embed = embed)

async def setup(bot):
    await bot.add_cog(scraperCog(bot), guilds = [discord.Object(id = serverId)])