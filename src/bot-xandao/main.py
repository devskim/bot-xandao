from typing import Coroutine, Literal, Optional
import discord
import discord.ext
from discord.ext.commands import Bot, Context, Greedy
from discord.ext import commands
from cogs.general import XandaoCog
from cogs.guardioes import GuardiaoCog
from cogs.ungabunga import UngaBungaCog
from cogs.voice import VoiceCog

from logger import log
from config import DISCORD_TOKEN, COMMANDS_CHANNEL


class MyClient(Bot):
    def __init__(self, *, intents: discord.Intents) -> None:
        super().__init__(intents=intents, command_prefix="?")

    async def setup_hook(self) -> None:

        await client.load_extension("cogs.general", package="cogs")
        await client.load_extension("cogs.guardioes", package="cogs")
        await client.load_extension("cogs.ungabunga", package="cogs")
        await client.load_extension("cogs.voice", package="cogs")
        log.info("Bot Setup Done!")

    async def load_cogs(self):
        await self.load_extension("commands.Commands")
        return


intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = MyClient(intents=intents)


@client.command()
async def ping(ctx: Context):
    await ctx.reply("Pong")


@client.command()
@commands.is_owner()
@commands.guild_only()
async def sync(
    ctx: Context,
    guilds: Greedy[discord.Object],
    spec: Optional[Literal["~", "*", "^"]] = None,
) -> None:
    if ctx.channel.id != COMMANDS_CHANNEL:
        log.info("Sync used not in the commands channel.")
        return

    log.info("Starting sync")
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        syncstr = f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        await ctx.send(embed=discord.Embed(description=syncstr))
        log.info(syncstr)
        return
    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    many_guilds_str = f"Synced the tree to {ret}/{len(guilds)}."

    await ctx.send(embed=discord.Embed(description=many_guilds_str))

    log.info(many_guilds_str)


@client.event
async def on_ready():
    assert client.user is not None
    log.info(f"Logged in as {client.user} (ID: {client.user.id})")
    print("------")


async def setup_bot():
    await client.add_cog(UngaBungaCog(client))
    await client.add_cog(XandaoCog(client))
    await client.add_cog(GuardiaoCog(client))
    await client.add_cog(VoiceCog(client))
    return client


async def run_bot(token) -> Coroutine:
    client = await setup_bot()
    return client.start(token)


client.run(DISCORD_TOKEN)
