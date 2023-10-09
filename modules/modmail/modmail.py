import discord
import math
from discord.ext import commands
from utils import genUtils
from modules.modmail.mailtypes import *
from data import botResponses
from data.localdata import *

async def sendMessage(bot: discord.Client, ctx: commands.Context):
    def getRecipientFromStarterEmbed(ctx: commands.Context, msg: discord.Message) -> discord.User | discord.Member:
        assert ctx.guild
        recipient_mention = msg.embeds[0].footer.text
        assert recipient_mention
        recipient = genUtils.memberByName(ctx.guild, recipient_mention)
        assert recipient

        return recipient

    def getRecipientFromStarterMessage(ctx: commands.Context, msg: discord.Message) -> discord.User | discord.Member:
        member_mention = starter_message.content.strip()
        member_id = genUtils.mentionToId(member_mention)
        if not member_id: raise commands.CommandError(f"Cannot find user {member_mention}.")
        recipient = bot.get_user(member_id)
        assert recipient

        return recipient

    assert ctx.guild
    assert isinstance(ctx.author, discord.Member)
    if not genUtils.isStaff(ctx.author): raise commands.CommandError(botResponses.NOT_STAFF_ERROR())  

    if not isinstance(ctx.channel, discord.Thread): raise commands.CommandError(botResponses.MAIL_NOT_IN_THREAD())
    if not isinstance(ctx.channel.parent, discord.ForumChannel): raise commands.CommandError(botResponses.MAIL_NOT_IN_FORUM())
    if not ctx.channel.parent.id == id_mail_channel: raise commands.CommandError(botResponses.MAIL_NOT_IN_MAIL_CHANNEL())
    if not ctx.message.reference: raise commands.CommandError(botResponses.MAIL_NO_REPLY_MESSAGE())

    recipient: discord.User | discord.Member
    recipient_mention: str
    starter_message = await ctx.channel.fetch_message(ctx.channel.id)
    assert isinstance(starter_message, discord.Message)
    if len(starter_message.embeds) > 0:
        recipient = getRecipientFromStarterEmbed(ctx, starter_message)
        recipient_mention = recipient.mention
    else:
        recipient = getRecipientFromStarterMessage(ctx, starter_message)
        recipient_mention = recipient.mention

    msg_reference = ctx.message.reference
    assert msg_reference.message_id
    mail_message = await ctx.fetch_message(msg_reference.message_id)

    staff_member_count: int = 0
    for role in ctx.guild.roles:
        if role.id == StaffRoles.Staff:
            staff_member_count = len(role.members)

    needed_staff_count = math.ceil(staff_member_count/3)
    footer = f"---\nReply to this embed to respond to this mod mail.\nTicket ID: {genUtils.encode(ctx.channel.id)}"
    for reaction in mail_message.reactions:
        if reaction.emoji == "📨" and reaction.count >= needed_staff_count:
            await recipient.send(embed=botResponses.MAIL_EMBED_RECEIVED(f"**Mail van {ctx.author.name}, namens de staff**.", mail_message.content, footer))
            await ctx.send(botResponses.MAIL_SENT(recipient_mention))
            break
    else:
        await ctx.send(botResponses.MAIL_NOT_APPROVED(needed_staff_count))


async def sendMailWizard(bot: discord.Client, msg: discord.Message):
    channel = msg.author.dm_channel
    assert channel

    await msg.channel.send(botResponses.MAIL_ISANON())

    def anonCheck(m: discord.Message) -> bool:
        if m.channel.id != channel.id: return False
        if m.content.strip().lower() in ["yes", "no"]:
            return True
        return False

    msg = await bot.wait_for("message", check=anonCheck, timeout=30)
    if msg.content.lower() == "yes": 
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

    msg = await bot.wait_for("message", check=mailTypeCheck, timeout=30)
    mailtype = MailType(int(msg.content))

    await msg.channel.send(botResponses.MAIL_TYPE_YOUR_MESSAGE())
    def messageCheck(m: discord.Message) -> bool: return m.channel.id == channel.id and m.author == msg.author
    finalmsg = await bot.wait_for("message", check=messageCheck, timeout=30*60)

    await msg.channel.send(botResponses.MAIL_TYPE_SEND())
    def sendCheck(m: discord.Message) -> bool:
        if m.channel.id != channel.id: return False
        if m.content.strip().lower() == "send":
            return True
        return False

    await bot.wait_for("message", check=sendCheck)

    mail = newMail(finalmsg.content, mailtype, author)

    addNewMailToInbox(mail)

    mail_channel = bot.get_channel(id_mail_channel)
    assert isinstance(mail_channel, discord.channel.ForumChannel)

    mail_title = f"{mailtype.name.title()} @ {datetime.now().strftime('%m/%d/%Y; %H:%M')}"
    if author != "/": mail_title += f" by {author}"
    
    thread_w_message = await mail_channel.create_thread(
        embed=botResponses.MAIL_EMBED_RECEIVED("Mail received", mail.message, mention_author), 
        name=mail_title,
    )
    if author != "/": await thread_w_message.thread.send(botResponses.MAIL_RESPOND())


    def _getTag(enum: ModMailRoles) -> discord.ForumTag:
        tag = mail_channel.get_tag(enum)
        assert isinstance(tag, discord.ForumTag)
        return tag

    tags: list[discord.ForumTag] = []

    tags.append(_getTag(ModMailRoles.In))

    match mailtype:
        case MailType.OTHER:
            pass
        case MailType.FEEDBACK:
            tags.append(_getTag(ModMailRoles.Server))
            tags.append(_getTag(ModMailRoles.Mod))
        case MailType.REPORT:
            tags.append(_getTag(ModMailRoles.Report))
            tags.append(_getTag(ModMailRoles.Mod))
        case MailType.NIVEAU:
            tags.append(_getTag(ModMailRoles.Niveau))
        case MailType.SESSIE:
            tags.append(_getTag(ModMailRoles.Server))
        case MailType.BOT:
            tags.append(_getTag(ModMailRoles.Server))

    await thread_w_message.thread.add_tags(*tags)

    await msg.channel.send(botResponses.MAIL_SENT("the staff team"))