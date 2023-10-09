from discord.ext import commands
import discord
from data.localdata import ModMailRoles, id_server, id_mail_channel
from modules.modmail.mailtypes import *
import modules.modmail.modmail as modmail
from data import botResponses
from utils import genUtils

class mailCog(commands.Cog):
    def __init__(self, bot):
        self.bot: discord.Client = bot
        self.active_members: list[discord.Member|discord.User] = []

        self.sendmail_command = "sendmail"

    @commands.Cog.listener()
    async def on_ready(self):
        print("Mail Cog is ready")
        self.active_members = []

    @commands.command()
    @genUtils.catcherrors
    async def sendmessage(self, ctx: commands.Context):
        try: await modmail.sendMessage(self.bot, ctx)
        except commands.CommandError as ce: await ctx.send(ce.args[0])

    @commands.Cog.listener()
    async def on_thread_create(self, thread: discord.Thread):
        assert thread.owner
        if thread.owner.bot: return

        if isinstance(thread, discord.Thread) and isinstance(thread.parent, discord.ForumChannel):
            if thread.parent.id == id_mail_channel:
                out_tag = thread.parent.get_tag(ModMailRoles.Out)
                await thread.send(botResponses.MAIL_REPLY_WITH_SENDMESSAGE())
                if out_tag: await thread.add_tags(out_tag)

                starter_message = thread.starter_message
                assert(starter_message)
                person = genUtils.mentionToId(starter_message.content.strip().split()[0])
                if not self.bot.get_user(person):
                    await thread.send(botResponses.MAIL_NO_USER_FOUND_IN_THREAD())


    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.author.bot: return
        if msg.author in self.active_members: return

        dm_channel = msg.author.dm_channel
        if not dm_channel: dm_channel = await msg.author.create_dm()

        if msg.reference:
            assert(msg.reference.message_id)
            responded_message = await dm_channel.fetch_message(msg.reference.message_id)
            assert(isinstance(responded_message, discord.Message)) 

            if len(responded_message.embeds) > 0:
                embed = responded_message.embeds[0]
                footer_text = embed.footer.text
                assert(footer_text)
                ticket_id = footer_text.split("\n")[-1].split()[-1]

                thread_id = genUtils.decode(ticket_id)
                thread = await self.bot.fetch_channel(thread_id)
                assert(isinstance(thread, discord.Thread))

                await dm_channel.send("Your reply has been sent to the staff team.")
                await thread.send(embed=botResponses.MAIL_EMBED_RECEIVED("Mail received", msg.content, msg.author.name))
            return

        if msg.channel.id == dm_channel.id:
            if msg.content.strip().lower() == self.sendmail_command:
                #Check for spam
                amount_sent_today = 0 
                async for msg_in_history in dm_channel.history():
                    if msg_in_history.content == botResponses.MAIL_SENT("the staff team") and \
                        datetime.today().replace(tzinfo=None).date() == msg_in_history.created_at.replace(tzinfo=None).date():
                        amount_sent_today += 1
                if amount_sent_today >= 3:
                    return await dm_channel.send(botResponses.MAIL_NO_SPAM())

                try:
                    self.active_members.append(msg.author)
                    await modmail.sendMailWizard(self.bot, msg)
                except TimeoutError:
                    await dm_channel.send(botResponses.MAIL_TIMED_OUT())
                finally:
                    self.active_members.remove(msg.author)
            else:
                await msg.channel.send(botResponses.MAIL_USE_SENDMAIL(self.sendmail_command))

async def setup(bot):
    await bot.add_cog(mailCog(bot), guilds = [discord.Object(id = id_server)])