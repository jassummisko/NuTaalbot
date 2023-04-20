import discord
from discord.ext import commands
from data.localdata import applicationId, serverId

with open(".token", "r") as file: TOKEN = file.read()

intents = discord.Intents.all()
intents.members = True

COGNAMES = [
    #"faqCog",
    #"mainCog",
    #"roleManagerCog",
    #"channelManagerCog",
    #"loggerCog",
    "debugCog",
    #"scraperCog",
    "quoteCog"
]

class Taalbot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!!!", 
            intents=intents, 
            member_cache_flags=discord.MemberCacheFlags.all(), 
            help_command=None,
            application_id = applicationId,
            case_insensitive=True
        )
    
    async def setup_hook(self):
        for cogname in COGNAMES:
            await bot.load_extension(f'cogs.{cogname}')
        await bot.tree.sync(guild = discord.Object(id = serverId))

bot = Taalbot()
bot.run(TOKEN)