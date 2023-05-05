import discord, \
    data.botResponses as botResponses, \
    utils.genUtils as genUtils
from discord.ext import commands
from data.localdata import serverId
from data.localdata import serverId, logChannelId, welcomeChannelId

class mainCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logChannel: discord.TextChannel
        self.welcomeChannel: discord.TextChannel

    @commands.Cog.listener()
    async def on_ready(self):
        print("Logger Cog is ready")

        logChannel = self.bot.get_channel(logChannelId)
        assert isinstance(logChannel, discord.TextChannel), \
            Exception(f"Text channel with ID {logChannelId} not found")
        self.logChannel = logChannel
        
        welcomeChannel = self.bot.get_channel(welcomeChannelId)
        assert isinstance(welcomeChannel, discord.TextChannel), \
            Exception(f"Text channel with ID {welcomeChannelId} not found")
        self.welcomeChannel = welcomeChannel

        await logChannel.send(f"Bleep bloop. I am here, ready to serve requests!")

    @commands.Cog.listener()
    @genUtils.catcherrors
    async def on_member_join(self, member: discord.Member):
        await self.welcomeChannel.send(f"Hallo, {member.mention}. Welkom op **Nederlands Leren**!")
        await self.logChannel.send(f"**{member.mention}** has joined.")

    @commands.Cog.listener()
    @genUtils.catcherrors
    async def on_member_remove(self, member: discord.Member):
        await self.logChannel.send(f"**{member.name}#{member.discriminator}** has left.")

    @commands.command(description="Says hi to the bot!")
    async def hi(self, ctx: commands.Context):
        await ctx.send(botResponses.ELK_ZINNEN_DAH)

async def setup(bot):
    await bot.add_cog(mainCog(bot), guilds = [discord.Object(id = serverId)])
