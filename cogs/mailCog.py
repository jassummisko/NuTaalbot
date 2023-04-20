from discord.ext import commands
from discord import app_commands
import discord
from data.localdata import serverId
import data.quotes as quotes
import utils.genUtils as genUtils
import modules.beginners.beginners as beginners
from discord.ext.commands import CommandError

class mailCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Mail Cog is ready")

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot: return
        if not (channel := msg.author.dm_channel):
            channel = await msg.author.create_dm()
        if msg.channel.id == channel.id:
            await msg.reply("ok!")

async def setup(bot):
    await bot.add_cog(mailCog(bot), guilds = [discord.Object(id = serverId)])