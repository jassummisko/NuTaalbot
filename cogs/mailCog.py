from discord.ext import commands
import discord
from data.localdata import serverId, mailChannelId, staffRoles
from modules.modmail.modmail import *
from data import botResponses
from utils import genUtils
import math

class mailCog(commands.Cog):
    def __init__(self, bot):
        self.bot: discord.Client = bot
        self.activeMembers: list[discord.Member|discord.User] = []

    @commands.Cog.listener()
    async def on_ready(self):
        print("Mail Cog is ready")
        self.activeMembers = []

    @commands.command()
    async def sendmessage(self, ctx: commands.Context):
        assert ctx.guild
        assert isinstance(ctx.author, discord.Member)
        if not genUtils.isStaff(ctx.author): return await ctx.send(botResponses.NOT_STAFF_ERROR())  

        if not isinstance(ctx.channel, discord.Thread): return await ctx.send("Not in thread.")
        if not isinstance(ctx.channel.parent, discord.ForumChannel): return await ctx.send("Not in forum channel.")
        if not ctx.channel.parent.id == mailChannelId: return await ctx.send("Not in mail channel.")

        recipient: discord.User | discord.Member | None
        recipient_mention: str | None
        starter_message = await ctx.channel.fetch_message(ctx.channel.id)
        assert isinstance(starter_message, discord.Message)
        if len(starter_message.embeds) > 0:
            recipient_mention = starter_message.embeds[0].footer.text
            assert recipient_mention
            recipient = genUtils.memberByName(ctx.guild, recipient_mention)
            assert recipient
        else:
            member_mention = starter_message.content.removesuffix(".").split()[-1]
            member_id = genUtils.mentionToId(member_mention)
            if not member_id: return await ctx.send(f"Cannot find user {member_mention}.")
            recipient = self.bot.get_user(member_id)
            assert recipient
            recipient_mention = recipient.mention

        msg_reference = ctx.message.reference
        if not msg_reference: return await ctx.send("No reply message found.")

        assert msg_reference.message_id
        mail_message = await ctx.fetch_message(msg_reference.message_id)

        staff_member_count: int = 0
        for role in ctx.guild.roles:
            if role.id == staffRoles.Staff:
                staff_member_count = len(role.members)

        needed_staff_count = math.ceil(staff_member_count/3)
        for reaction in mail_message.reactions:
            if reaction.emoji == "📨" and reaction.count >= needed_staff_count:
                await recipient.send(embed=botResponses.MAIL_EMBED_RECEIVED(mail_message.content, ctx.author.name))
                await ctx.send(f"Message sent to user {recipient_mention}.")
                break
        else:
            await ctx.send(f"The message has not been approved by enough staff members ({needed_staff_count})")

    @commands.Cog.listener()
    async def on_thread_create(self, thread: discord.Thread):
        assert thread.owner
        if thread.owner.bot: return

        if isinstance(thread, discord.Thread) and isinstance(thread.parent, discord.ForumChannel):
            if thread.parent.id == mailChannelId:
                await thread.send("Reply to the message using the command `!!!sendmessage` send it.")

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.author.bot: return
        if msg.author in self.activeMembers: return

        dm_channel = msg.author.dm_channel
        if not dm_channel: dm_channel = await msg.author.create_dm()
        if msg.channel.id == dm_channel.id:
            if msg.content.strip() == "sendmail":
                #Check for spam
                amount_sent_today = 0 
                async for msg_in_history in dm_channel.history():
                    if msg_in_history.content == botResponses.MAIL_SENT() and \
                        (datetime.today().replace(tzinfo=None) - msg_in_history.created_at.replace(tzinfo=None)).days == 0:
                        amount_sent_today += 1
                if amount_sent_today >= 3:
                    return await dm_channel.send("You've already sent 3 modmails today. Please wait until tomorrow.")

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
        if msg.content == "yes": 
            author = "/"
            mention_author = "Anonymous"
        else: 
            author = msg.author.name
            mention_author = msg.author.name

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

        mail = newMail(finalmsg.content, mailtype, author)

        addNewMailToInbox(mail)

        mail_channel = self.bot.get_channel(mailChannelId)
        assert isinstance(mail_channel, discord.channel.ForumChannel)

        mail_title = f"{mailtype.name.title()} @ {datetime.now().strftime('%m/%d/%Y; %H:%M')}"
        if author != "/": mail_title += f" by {author}"
        
        await mail_channel.create_thread(
            embed=botResponses.MAIL_EMBED_RECEIVED(mail.message, mention_author), 
            name=mail_title,
        )
        await msg.channel.send(botResponses.MAIL_SENT())

async def setup(bot):
    await bot.add_cog(mailCog(bot), guilds = [discord.Object(id = serverId)])