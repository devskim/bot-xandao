from typing import cast

import discord
from discord import TextChannel
from discord.ext import commands

from config import (
    GERAL_CHANNEL,
    GUILD,
    LOG_CHANNEL,
)
from emb.embeds import (
    base_log_embed,
    LogDict,
)


class CommonCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def log(
        self,
        message: str | LogDict,
        *,
        channel: discord.TextChannel | None | int = None,
    ):
        if channel is None:
            log_channel = self.bot.get_channel(LOG_CHANNEL) or await self.bot.fetch_channel(LOG_CHANNEL)

        else:
            if isinstance(channel, int):
                log_channel = self.bot.get_channel(channel) or await self.bot.fetch_channel(channel)

            elif isinstance(channel, TextChannel):
                log_channel = channel

        log_channel = cast(TextChannel, log_channel)
        embed = base_log_embed(message)
        await log_channel.send(content=None, embed=embed)

    async def end_interaction(self, interaction, ephemeral: bool = True, delete_after: float = 0.1):
        await interaction.response.send_message(content="Enviando...", ephemeral=ephemeral, delete_after=delete_after)

    async def get_geral_channel(self) -> discord.TextChannel | None:
        guild = self.bot.get_guild(GUILD.id) or await self.bot.fetch_guild(GUILD.id)

        geralchannel = cast(discord.TextChannel, guild.get_channel(GERAL_CHANNEL))

        if guild is None and geralchannel is None:
            raise TypeError("Guild or geralchannel not found: None")

        return geralchannel
