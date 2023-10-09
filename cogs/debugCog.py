import discord, \
    data.botResponses as botResponses, \
    utils.genUtils as genUtils
from discord.ext import commands
from data.localdata import id_server
from discord.ext.commands import CommandError

class debugCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Debug Cog is ready")

    @commands.command()
    async def reloadcog(self, ctx: commands.Context, cog: str):
        assert isinstance(ctx.author, discord.Member)
        if not genUtils.isStaff(ctx.author): raise CommandError(botResponses.NOT_STAFF_ERROR())
        await ctx.send(f"Reloading cog {cog}")
        try:
            await self.bot.reload_extension(f"cogs.{cog}")
            await ctx.send(f"Cog {cog} reloaded.")
        except Exception as e: await ctx.send(e) # type: ignore

    @commands.command()
    async def loadcog(self, ctx: commands.Context, cog: str):
        assert isinstance(ctx.author, discord.Member)
        if not genUtils.isStaff(ctx.author): raise CommandError(botResponses.NOT_STAFF_ERROR())
        await ctx.send(f"Loading cog {cog}")
        try:
            await self.bot.load_extension(f"cogs.{cog}")
            await ctx.send(f"Cog {cog} loaded.")
        except Exception as e: await ctx.send(e) # type: ignore

    @commands.command()
    async def unloadcog(self, ctx: commands.Context, cog: str):
        assert isinstance(ctx.author, discord.Member)
        if not genUtils.isStaff(ctx.author): raise CommandError(botResponses.NOT_STAFF_ERROR())
        await ctx.send(f"Unloading cog {cog}")
        try:
            await self.bot.unload_extension(f"cogs.{cog}")
            await ctx.send(f"Cog {cog} unloaded.")
        except Exception as e: await ctx.send(e) # type: ignore

    @commands.command()
    async def resynctree(self, ctx: commands.Context):
        assert isinstance(ctx.author, discord.Member)
        if not genUtils.isStaff(ctx.author): raise CommandError(botResponses.NOT_STAFF_ERROR())
        await ctx.send(f"Resyncing tree")
        try:
            await self.bot.tree.sync(guild = discord.Object(id = id_server))
            await ctx.send(f"Tree resynced.")
        except Exception as e: await ctx.send(e) # type: ignore

    @commands.command()
    async def print_tags(self, ctx: commands.Context):
        assert isinstance(ctx.channel, discord.Thread)
        assert isinstance(ctx.channel.parent, discord.ForumChannel)

        forum = ctx.channel.parent

        buffer = ""
        for tag in forum.available_tags:
            buffer += f"{tag.emoji} - {tag.id}\n"

        await ctx.channel.send(buffer.strip())

    @commands.command()
    @genUtils.catcherrors
    async def debugtest(self, ctx: commands.Context):
        raise Exception("Test")

async def setup(bot):
    await bot.add_cog(debugCog(bot), guilds = [discord.Object(id = id_server)])