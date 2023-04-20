import discord, \
    utils.genUtils as genUtils
from discord.ext import commands
from data.localdata import serverId, logChannelId, welcomeChannelId

class loggerCog(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Logger Cog is ready")
        await self.bot.get_channel(logChannelId) \
            .send(f"Bleep bloop. I am here, ready to serve requests!")

    @commands.Cog.listener()
    @genUtils.catcherrors
    async def on_member_join(self, member: discord.Member):
        await self.bot.get_channel(welcomeChannelId) \
            .send(f"Hallo, {member.mention}. Welkom op **Nederlands Leren**!")
        await self.bot.get_channel(logChannelId) \
            .send(f"**{member.mention}** has joined.")

    @commands.Cog.listener()
    @genUtils.catcherrors
    async def on_member_remove(self, member: discord.Member):
        logChannel = self.bot.get_channel(logChannelId)
        await logChannel.send(f"**{member.name}#{member.discriminator}** has left.")

async def setup(bot: discord.Client):
    await bot.add_cog(loggerCog(bot), guilds = [discord.Object(id = serverId)])