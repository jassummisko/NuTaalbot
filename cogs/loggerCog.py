from discord.ext import commands
import discord
from data.localdata import serverId, logChannelId, welcomeChannelId
import data.quotes as quotes
import utils.genUtils as genUtils
import modules.beginners.beginners as beginners

class loggerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Logger Cog is ready")

    @commands.Cog.listener()
    @genUtils.catcherrors
    async def on_member_join(self, member: discord.Member):
        await self.bot.get_channel(welcomeChannelId) \
            .send(f"Hallo, {member.mention}. Welkom op **Nederlands Leren**!")
        await self.bot.get_channel(logChannelId) \
            .send(f"**{member.name}** has joined.")

    @commands.Cog.listener()
    @genUtils.catcherrors
    async def on_member_remove(self, member: discord.Member):
        logChannel = self.bot.get_channel(logChannelId)
        await logChannel.send(f"**{member.name}** has left.")

async def setup(bot):
    await bot.add_cog(loggerCog(bot), guilds = [discord.Object(id = serverId)])