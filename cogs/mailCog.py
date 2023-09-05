from enum import member
from discord.app_commands import Command
from discord.ext import commands
import discord
from discord.ext.commands import CommandError
from data.localdata import serverId, logChannelId
from modules.modmail.modmail import *
from data import botResponses
from utils import genUtils

class mailCog(commands.Cog):
    def __init__(self, bot):
        self.bot: discord.Client = bot
        self.activeMembers: list[discord.Member|discord.User] = []

    @commands.Cog.listener()
    async def on_ready(self):
        print("Mail Cog is ready")
        self.activeMembers = []

    @commands.command()
    async def draftmessage(self, ctx: commands.Context, user: discord.User, *arg: str):
        assert isinstance(ctx.author, discord.Member)
        if not genUtils.isStaff(ctx.author): raise CommandError(botResponses.NOT_STAFF_ERROR()) 

        channel = ctx.channel
        thread_name = " ".join(arg)
        assert isinstance(channel, discord.TextChannel)

        msg = await channel.send(f"Drafting message to user {user.mention}.")

        thread = await msg.create_thread(name=thread_name)
        await thread.send("Draft your message below. Reply to it with \"!!!sendmessage\"to send it.")

        #Should I add a staff channel check?

    @commands.command()
    async def sendmessage(self, ctx: commands.Context):
        assert isinstance(ctx.author, discord.Member)
        if not genUtils.isStaff(ctx.author): return await ctx.send(botResponses.NOT_STAFF_ERROR())  

        if not isinstance(ctx.channel, discord.Thread): return await ctx.send("Not in thread.")

        starter_message = ctx.channel.starter_message
        assert starter_message
        member_mention = starter_message.content.removesuffix(".").split()[-1]
        member_id = genUtils.mentionToId(member_mention)
        if not member_id: return await ctx.send(f"Cannot find user {member_mention}.")
        recipient = self.bot.get_user(member_id)
        assert recipient

        msg_reference = ctx.message.reference
        if not msg_reference: return await ctx.send("No reply message found.")

        assert msg_reference.message_id
        mail_message = await ctx.fetch_message(msg_reference.message_id)

        await recipient.send(mail_message.content)
        await ctx.send(f"Message sent to user {recipient.mention}.")

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.author.bot: return
        if msg.author in self.activeMembers: return

        dm_channel = msg.author.dm_channel
        if not dm_channel: dm_channel = await msg.author.create_dm()
        if msg.channel.id == dm_channel.id:
            if msg.content.strip() == "sendmail":
                try:
                    self.activeMembers.append(msg.author)
                    await self.doMail(msg)
                finally:
                    self.activeMembers.remove(msg.author)
            else:
                await msg.channel.send("If you want to send mod mail, first type the message \"sendmail\".")

    async def doMail(self, msg: discord.Message):
        channel = msg.author.dm_channel
        assert channel

        await msg.channel.send(botResponses.MAIL_ISANON())

        def anonCheck(m: discord.Message) -> bool:
            if m.channel.id != channel.id: return False
            if m.content.strip() in ["yes", "no"]:
                return True
            return False

        msg = await self.bot.wait_for("message", check=anonCheck, timeout=30)
        if msg.content == "yes": author = "/"
        else: author = msg.author.name

        await msg.channel.send(botResponses.MAIL_CHOOSE_MAILTYPE())

        def mailTypeCheck(m: discord.Message) -> bool:
            if m.channel.id != channel.id: return False
            if m.content.isnumeric():
                selection = int(m.content)
                if selection in [e.value for e in MailType]:
                    return True
            return False

        msg = await self.bot.wait_for("message", check=mailTypeCheck, timeout=30)
        mailtype = MailType(int(msg.content))

        await msg.channel.send(botResponses.MAIL_TYPE_YOUR_MESSAGE())
        def messageCheck(m: discord.Message) -> bool: return m.channel.id == channel.id and m.author == msg.author
        finalmsg = await self.bot.wait_for("message", check=messageCheck, timeout=30*60)

        await msg.channel.send(botResponses.MAIL_TYPE_SEND())
        def sendCheck(m: discord.Message) -> bool:
            if m.channel.id != channel.id: return False
            if m.content.strip() == "send":
                return True
            return False

        await self.bot.wait_for("message", check=sendCheck)

        mail = NewMail(finalmsg.content, mailtype, author)

        AddNewMailToInbox(mail)

        logChannel = self.bot.get_channel(logChannelId)
        assert isinstance(logChannel, discord.channel.TextChannel)
        await logChannel.send(embed=botResponses.MAIL_EMBED_RECEIVED(mail.message, mail.author))
        await msg.channel.send(botResponses.MAIL_SENT())

async def setup(bot):
    await bot.add_cog(mailCog(bot), guilds = [discord.Object(id = serverId)])