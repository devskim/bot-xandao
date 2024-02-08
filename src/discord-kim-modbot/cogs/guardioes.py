import discord
from discord import app_commands
from discord.ext import commands

from config import (
    BALCAO_CHANNEL,
)

from emb.embeds import report_embed

from .common import CommonCog


class GuardiaoGroup(app_commands.Group):
    ...


class GuardiaoCog(CommonCog):
    guardiao = GuardiaoGroup(name="guardiao", description="Comandos para os guardiões")

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.bot.tree.add_command(app_commands.ContextMenu(name="A. Reportar", callback=self.report_message))

    async def report_message(self, interaction: discord.Interaction, message: discord.Message):
        content = f"Obrigado por reportar a mensagem de {message.author.mention} para nossa moderação."
        await interaction.response.send_message(content=content, ephemeral=True, delete_after=3.0)

        embed, url_view = report_embed(interaction, message)

        channel = self.bot.get_channel(BALCAO_CHANNEL)

        if isinstance(channel, discord.TextChannel):
            if message.attachments[0].content_type.startswith("video"):
                await channel.send(content=f"Vídeo reportado: \n {message.attachments[0].proxy_url}")
            await channel.send(embed=embed, view=url_view)
            return


async def setup(bot):
    await bot.add_cog(GuardiaoCog(bot))
