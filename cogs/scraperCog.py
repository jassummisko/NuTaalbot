from typing import final
import discord, \
    data.botResponses as botResponses, \
    utils.genUtils as genUtils
from modules.scraper.dictionary import CreateEntry, GetAppropriateEmbed 
from discord.ext import commands
from discord import app_commands
from data.localdata import id_server
from modules.scraper.scraper import *
from modules.scraper.woordenlijst import *
from discord.ext import menus # type: ignore
import pandas as pd # type: ignore

def get_clean_entries(entry: str) -> list[str]:
    SYMBOLS_TO_REMOVE = ";*/,"
    for s in SYMBOLS_TO_REMOVE:
        entry = entry.replace(s, "")
    return entry.strip().split()

class scraperCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Loading dictionary in memory...")
        try:
            #sheets = [x for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
            self.file = pd.read_excel("modules/scraper/wnt2.xlsx", sheet_name = None)
        except Exception as e:
            print("Loading failed. Reading:")
            print(e)
        else:
            print("Loading successful")

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
        scraped: list[WordEntry] | None = checkWoordenlijst(woord)
        words: list[WordEntry] = []
        embed = discord.Embed(title=f"Resultaten voor \"{woord}\"")
        
        if not scraped: message = botResponses.DEHET_NOWORD(woord)
        else: words: list[WordEntry] = [word for word in scraped if word.partOfSpeech == "znw"]
        
        if (not words) or len(words) == 0: message = botResponses.DEHET_NONOUN(woord)
        elif len(words) == 1:
            message = botResponses.DEHET_SINGLEWORD(words[0].grammaticalInfo['art'], words[0].lemma)
        elif len(words) > 1:
            message = ""
            for word in words:
                message += botResponses.DEHET_MULTIWORD(
                    word.grammaticalInfo['art'],
                    word.lemma,
                    word.grammaticalInfo['gloss'],
                )
        else: message = "ERROR"

        embed.description = message.strip()
        await i9n.response.send_message(embed = embed)

    @app_commands.command(name="watbetekent", description="Wat betekent het woord ...?")
    @app_commands.describe(woord="Het woord")
    @genUtils.catcherrors
    async def watbetekent(self, i9n: discord.Interaction, woord: str):
        woord = woord.lower().strip()
        found_entries = []
        for _, sheet in self.file.items():
            for _, entry in sheet.iterrows():
                if not "Lemma" in entry: break
                lemma = str(entry["Lemma"])
                forms = get_clean_entries(str(entry["Vormen"]))
                if woord == lemma:
                    found_entries.append(entry)
                    continue

                if woord in forms:
                    found_entries.append(entry)
                    continue

        test_embeds = []

        for entry in found_entries:
            test_embeds.append(GetAppropriateEmbed(CreateEntry(entry)))

        final_embed = menus.MenuPages(genUtils.MultiPageEmbed(test_embeds, per_page = 1))

        ctx = await self.bot.get_context(i9n)
        await i9n.response.send_message("Command worked")
        await final_embed.start(ctx)

async def setup(bot):
    await bot.add_cog(scraperCog(bot), guilds = [discord.Object(id = id_server)])