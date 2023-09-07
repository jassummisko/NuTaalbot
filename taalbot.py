import discord
from discord.ext import commands
from data.localdata import id_application, id_server

intents = discord.Intents.all()
intents.members = True

cogsToLoad = [
    #"faqCog",
    #"mainCog",
    #"roleManagerCog",
    #"channelManagerCog",
    #"debugCog",
    #"scraperCog",
    "mailCog",
]

class Taalbot(commands.Bot):
    def __init__(self, intents, cogNames: list[str]):
        self.cogNames = cogNames
        super().__init__(
            command_prefix="!!!", 
            intents=intents, 
            member_cache_flags=discord.MemberCacheFlags.all(), 
            help_command=None,
            application_id = id_application,
            case_insensitive=True
        )
    
    async def setup_hook(self):
        for cogname in self.cogNames:
            await self.load_extension(f'cogs.{cogname}')
        await self.tree.sync(guild = discord.Object(id = id_server))

BOT = Taalbot(intents, cogsToLoad)