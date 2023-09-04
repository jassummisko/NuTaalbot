import discord, \
    data.botResponses as botResponses, \
    utils.genUtils as genUtils
from discord.ext import commands
from discord import app_commands
from data.localdata import serverId
from data.localdata import serverId, logChannelId, welcomeChannelId
from modules.beginners.beginners import *
from modules.modmail.modmail import NewMail, AddNewMailToInbox

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
        await ctx.send(botResponses.ELK_ZINNEN_DAH())

    @app_commands.command(name="hoelaat", description="Hoe laat is het?")
    @genUtils.catcherrors
    async def hoelaat(self, i9n: discord.Interaction):
        await i9n.response.send_message(content=getCurrentTimeInDutch())

    @app_commands.command(name="sendmail", description="Send a message to the mods.")
    @app_commands.describe(message="The message you want to send", anon = "Whether the message should be anonymous (defaults to True).")
    @genUtils.catcherrors
    async def sendmail(self, i9n: discord.Interaction, message: str, anon: bool = True):
        logChannel = self.bot.get_channel(logChannelId)
        assert isinstance(logChannel, discord.channel.TextChannel)
        author = "ANONYMOUS"

        if not anon:
            assert i9n.message
            author = i9n.message.author.name

        mail = NewMail(message, author)

        AddNewMailToInbox(mail)

        await logChannel.send(embed=botResponses.EMBED_MAIL_RECEIVED(mail.message, mail.author))

        await i9n.response.send_message(botResponses.MOD_MAIL_SENT(), ephemeral=True)


async def setup(bot):
    await bot.add_cog(mainCog(bot), guilds = [discord.Object(id = serverId)])
