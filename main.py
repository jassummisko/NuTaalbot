import asyncio
import os
import discord
from discord.ext import commands

with open(".token", "r") as file: TOKEN = file.read()

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(
    command_prefix="!", 
    intents=intents, 
    member_cache_flags=discord.MemberCacheFlags.all(), 
    help_command=None,
    case_insensitive=True
)

COGNAMES = [
    "faqCog",
    "mainCog",
    #"channelCheckerCog",
    "channelManagerCog",
]

async def load():
    for cogname in COGNAMES:
        await bot.load_extension(f'cogs.{cogname}')

async def main():
    await load()
    await bot.start(TOKEN)

asyncio.run(main())