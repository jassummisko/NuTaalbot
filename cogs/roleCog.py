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
        view = await roleSelectionView(i9n.guild, lambda x:"Niveau" in x.name, 1)
        await i9n.response.send_message("Here you go!", view=view)

    @app_commands.command(name="debug_onboard", description="OK")
    @utils.catcherrors
    async def debug_onboard(self, i9n: discord.Interaction, member: discord.Member):
        await i9n.response.send_message(f"Onboarding user {member.name}")
        
        dropdown = discord.ui.Select(
            max_values = 1, 
            placeholder = "Test1", 
            options = [
                discord.SelectOption(label="test1"),
                discord.SelectOption(label="test2"),
                discord.SelectOption(label="test3"),
            ],
        )
        
        async def callback(i9n: discord.Interaction):
                        
            dropdown1 = discord.ui.Select(
                max_values = 1, 
                placeholder = "Test23", 
                options = [
                    discord.SelectOption(label="test1"),
                    discord.SelectOption(label="test2"),
                    discord.SelectOption(label="test3"),
                ],
            )

            async def callback(i9n: discord.Interaction):
                print(dropdown1.values[0])

            dropdown1.callback = callback
            view = discord.ui.View()
            view.add_item(dropdown1)

            if dropdown.values[0] == "test1": 
                await i9n.response.send_message(content="OK")
                await i9n.message.reply(content="f", view=view)

        dropdown.callback = callback
        view = discord.ui.View()
        view.add_item(dropdown)
        await i9n.user.send(content="f", view=view)

async def setup(bot):
    await bot.add_cog(roleCog(bot), guilds = [discord.Object(id = serverID)])