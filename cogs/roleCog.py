import discord
from discord import app_commands
from localdata import serverId, countryRoleColor
from discord.ext import commands
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
        countryRoles = [role for role in i9n.guild.roles if role.color == countryRoleColor]
        role = [role for role in countryRoles if role.name.upper() == land.upper()]
        if len(role) > 0: await i9n.user.add_roles(role[0])
        else: responseMsg = f"Er is geen land met de naam {land}"
        await i9n.response.send_message(responseMsg)

   # @landrol.autocomplete('land')
   # async def landrol_autocomplete(self, i9n: discord.Interaction, current: str):
   #     try: 
   #         landen = [role.name for role in i9n.guild.roles if role.color == countryRoleColor]
   #         roleOptions = [land for land in landen if current.lower() == land[0:len(current)].lower()]
   #         nOptions = min(8, len(roleOptions))
   #         return roleOptions[0:nOptions]
   #     except Exception as e:
   #         print(e)

    @app_commands.command(name="niveaurol", description="Assign level roles")
    @utils.catcherrors
    async def niveaurol(self, i9n: discord.Interaction):
        await i9n.user.remove_roles(*[role for role in i9n.user.roles if "Niveau" in role.name])
        view = await roleSelectionView(i9n.guild, lambda x:"Niveau" in x.name, 1)
        await i9n.response.send_message("Here you go!", view=view)

async def setup(bot):
    await bot.add_cog(roleCog(bot), guilds = [discord.Object(id = serverId)])