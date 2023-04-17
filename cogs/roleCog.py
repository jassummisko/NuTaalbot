import discord
from discord import app_commands
from discord.app_commands import Choice
from localdata import serverId, countryRoleColor
from discord.ext import commands
from fuzzywuzzy import fuzz
import utils.utils as utils
from modules.roleAssigner.roleAssigner import *

class roleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Role Cog is ready")

    @app_commands.command(name="landrol", description="Assign country roles")
    @app_commands.describe(land="De naam van het land")
    @utils.catcherrors
    async def landrol(self, i9n: discord.Interaction, land: str):
        responseMsg = "Alsjeblieft!"
        await i9n.user.add_roles([role for role in i9n.guild.roles if role.name == land][0])
        await i9n.response.send_message(responseMsg)

    @landrol.autocomplete('land')
    async def landrol_autocomplete(self, i9n: discord.Interaction, current: str):
        try: 
            roles = sorted(
                [role.name for role in i9n.guild.roles if role.color == countryRoleColor], 
                key=(lambda role: fuzz.ratio(role.lower(), current.lower())), 
                reverse=True
            )
            return [Choice(name=role, value=role) for role in roles[:10]] 
        except Exception as e: print(e)

    @app_commands.command(name="niveaurol", description="Assign level roles")
    @utils.catcherrors
    async def niveaurol(self, i9n: discord.Interaction):
        await i9n.user.remove_roles(*[role for role in i9n.user.roles if "Niveau" in role.name])
        view = await roleSelectionView(i9n.guild, lambda x:"Niveau" in x.name, 1)
        await i9n.response.send_message("Here you go!", view=view)

async def setup(bot):
    await bot.add_cog(roleCog(bot), guilds = [discord.Object(id = serverId)])