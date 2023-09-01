import discord, asyncio, \
    data.botResponses as botResponses, \
    utils.genUtils as genUtils
from data.localdata import serverId, leerkrachtRoleId, countryRoleColor, pronounRoles
from discord import Interaction, Member, app_commands
from discord.ext import commands
from modules.roleManager.roleManager import *
from discord.app_commands import Choice
from fuzzywuzzy import fuzz
from discord.ext.commands import CommandError

class roleManagerCog(commands.Cog):
    def __init__(self, bot):
        self.bot: discord.Client = bot
        self.rolesPendingRemoval: list[PendingEntry] = getRolesPendingRemoval()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Role Manager Cog is ready")

        guild = self.bot.get_guild(serverId)        
        assert guild
        queue = queuePendingRemovals(guild, self.rolesPendingRemoval)
        if len(queue) > 0: await asyncio.gather(*queue, return_exceptions=True) # type: ignore

    @app_commands.command(name="giveleerkrachtrole", description="Geef de leerkracht rol aan iemand")
    @app_commands.describe(user="username", duration="duration in minutes")
    @genUtils.catcherrors
    async def giveleerkrachtrole(self, i9n: Interaction, user: Member, duration: int = 180) -> None:
        assert i9n.guild
        assert isinstance(callingUser := i9n.user, discord.Member)
        assert (leerkrachtRole := i9n.guild.get_role(leerkrachtRoleId))

        if not genUtils.isStaff(callingUser): raise CommandError(botResponses.NOT_STAFF_ERROR()) 

        await giveTemporaryRole(self.rolesPendingRemoval, i9n, user, leerkrachtRole, duration)

    @app_commands.command(name="landrol", description="Assign country roles")
    @app_commands.describe(land="De naam van het land")
    @genUtils.catcherrors
    async def landrol(self, i9n: discord.Interaction, land: str):
        assert i9n.guild
        assert isinstance(callingUser := i9n.user, discord.Member)

        responseMsg = "Alsjeblieft!"
        await callingUser.add_roles([role for role in i9n.guild.roles if role.name == land][0])
        await i9n.response.send_message(responseMsg)

    @landrol.autocomplete('land') # type: ignore
    @genUtils.catcherrors
    async def landrol_autocomplete(self, i9n: discord.Interaction, current: str):
        assert i9n.guild
        roles = sorted(
            [role.name for role in i9n.guild.roles if role.color == countryRoleColor], 
            key=(lambda role: fuzz.ratio(role.lower(), current.lower())), 
            reverse=True
        )
        return [Choice(name=role, value=role) for role in roles[:10]] 

    @app_commands.command(name="niveaurol", description="Assign level roles")
    @app_commands.describe(niveau="CEFR niveau")
    @genUtils.catcherrors
    async def niveaurol(self, i9n: discord.Interaction, niveau: str = ""):
        assert i9n.guild
        assert isinstance(i9n.user, discord.Member)
        niveauRoles = [role for role in i9n.guild.roles if ("Niveau" in role.name) and not ("C+" in role.name)]
        niveauRoleNames = [role.name for role in niveauRoles]
        assert isinstance(callingUser := i9n.user, discord.Member)
        ###TODO: Make this less ugly.
        if niveau in niveauRoleNames:
            oldrole = [role for role in i9n.user.roles if "Niveau" in role.name][0]
            await i9n.user.remove_roles(oldrole)
            rolesToAdd = [role for role in niveauRoles if role.name == niveau]
            member = i9n.guild.get_member(i9n.user.id)
            assert member
            await member.add_roles(*rolesToAdd)
            await i9n.response.send_message(
                f"Changed role {oldrole.name} to {[role.name for role in rolesToAdd][0]} for user {i9n.user.mention}"
            )
        else:
            view = await niveauRolSelectionView(i9n.guild)
            await i9n.response.send_message("Here you go!", view=view)

    @niveaurol.autocomplete('niveau')
    async def niveaurol_autocomplete(self, i9n: discord.Interaction, current: str):
        assert i9n.guild
        niveauRoles = [role for role in i9n.guild.roles if ("Niveau" in role.name) and not ("C+" in role.name)]
        niveauRoleNames = [role.name for role in niveauRoles]
        return [Choice(name=role, value=role) for role in niveauRoleNames] 

    @app_commands.command(name="voornaamwoordrol", description="Assign pronoun roles")
    @app_commands.describe(vnw="The pronoun")
    @genUtils.catcherrors
    async def voornaamwoordrol(self, i9n: discord.Interaction, vnw: str):
        assert i9n.guild
        assert isinstance(callingUser := i9n.user, discord.Member)

        responseMsg = "Alsjeblieft!"
        await callingUser.add_roles([role for role in i9n.guild.roles if role.name == vnw][0])
        await i9n.response.send_message(responseMsg)

    @voornaamwoordrol.autocomplete('vnw') # type: ignore
    @genUtils.catcherrors
    async def voornaamwoordrol_autocomplete(self, i9n: discord.Interaction, _: str):
        roles: list
        assert i9n.guild
        roles = [i9n.guild.get_role(roleId) for roleId in pronounRoles] 
        print(roles)
        return [Choice(name=role.name, value=role.name) for role in roles] 

async def setup(bot):
    await bot.add_cog(roleManagerCog(bot), guilds=[discord.Object(id=serverId)])