from typing import cast

import discord
from discord import app_commands
from discord.ext import commands


from .common import CommonCog


class Xandao(app_commands.Group):
    ...


class XandaoCog(CommonCog):
    xandao = Xandao(name="xandao", description="Comandos gerais do Xandão")

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command()
    @app_commands.rename(text_to_send="text")
    @app_commands.describe(text_to_send="Text to send in the current channel")
    async def send(self, interaction: discord.Interaction, text_to_send: str):
        """Sends the text into the current channel."""

        chan = cast(discord.TextChannel, interaction.channel)
        await chan.send(text_to_send)
        await interaction.response.send_message("Enviando mensagem...", ephemeral=True, delete_after=0.1)


async def setup(bot):
    await bot.add_cog(XandaoCog(bot))
