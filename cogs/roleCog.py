import discord
from discord import app_commands
from localdata import serverID, countryRoleColor
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
    @utils.catcherrors
    async def landrol(self, i9n: discord.Interaction):
        view = await roleSelectionView(i9n.guild, lambda x:x.color == countryRoleColor)
        await i9n.response.send_message("Here you go!", view=view)

    @app_commands.command(name="niveaurol", description="Assign level roles")
    @utils.catcherrors
    async def niveaurol(self, i9n: discord.Interaction):
        user = i9n.user
        await user.remove_roles(*[role for role in user.roles if "Niveau" in role.name])
        view = await roleSelectionView(i9n.guild, lambda x:"Niveau" in x.name, max_values=1)
        await i9n.response.send_message("Here you go!", view=view)

async def setup(bot):
    await bot.add_cog(roleCog(bot), guilds = [discord.Object(id = serverID)])