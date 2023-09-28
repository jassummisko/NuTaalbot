import discord, \
    data.botResponses as botResponses, \
    utils.genUtils as genUtils
from discord.ext import commands
from discord import app_commands, channel
from data.localdata import id_server, id_log_channel, id_welcome_channel
from modules.beginners.beginners import *

class mainCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.log_channel: discord.TextChannel
        self.welcome_channel: discord.TextChannel

    @commands.Cog.listener()
    async def on_ready(self):
        print("Logger Cog is ready")

        log_channel = self.bot.get_channel(id_log_channel)
        assert isinstance(log_channel, discord.TextChannel), \
            Exception(f"Text channel with ID {id_log_channel} not found")
        self.log_channel = log_channel
        
        welcome_channel = self.bot.get_channel(id_welcome_channel)
        assert isinstance(welcome_channel, discord.TextChannel), \
            Exception(f"Text channel with ID {id_welcome_channel} not found")
        self.welcome_channel = welcome_channel

        await log_channel.send(f"Bleep bloop. I am here, ready to serve requests!")

    @commands.Cog.listener()
    @genUtils.catcherrors
    async def on_member_join(self, member: discord.Member):
        await self.welcome_channel.send(f"Hallo, {member.mention}. Welkom op **Nederlands Leren**!")
        await self.log_channel.send(f"**{member.mention}** has joined.")

    @commands.Cog.listener()
    @genUtils.catcherrors
    async def on_voice_state_update(self, member: discord.Member, m_before: discord.VoiceState, m_after: discord.VoiceState):
        assert m_before
        assert m_after

        #User joined
        if not m_before.channel and m_after.channel:
            await self.log_channel.send(
                botResponses.LOG_USER_JOINED_VC(
                    member.mention,
                    m_after.channel.mention,
                )
            )
        #User left
        elif m_before.channel and not m_after.channel:
            await self.log_channel.send(
                botResponses.LOG_USER_LEFT_VC(
                    member.mention,
                    m_before.channel.mention,
                )
            )
        #User switched VC
        elif m_before.channel and m_after.channel:
            if not (m_before.channel is m_after.channel):
                await self.log_channel.send(
                    botResponses.LOG_USER_LEFT_VC(
                        member.mention,
                        m_before.channel.mention,
                    )
                )
                await self.log_channel.send(
                    botResponses.LOG_USER_JOINED_VC(
                        member.mention,
                        m_after.channel.mention,
                    )
                )

    @commands.Cog.listener()
    @genUtils.catcherrors
    async def on_member_remove(self, member: discord.Member):
        await self.log_channel.send(f"**{member.name}#{member.discriminator}** has left.")

    @commands.command(description="Says hi to the bot!")
    async def hi(self, ctx: commands.Context):
        await ctx.send(botResponses.ELK_ZINNEN_DAH())

    @app_commands.command(name="hoelaat", description="Hoe laat is het?")
    @genUtils.catcherrors
    async def hoelaat(self, i9n: discord.Interaction):
        await i9n.response.send_message(content=getCurrentTimeInDutch())

async def setup(bot):
    await bot.add_cog(mainCog(bot), guilds = [discord.Object(id = id_server)])
