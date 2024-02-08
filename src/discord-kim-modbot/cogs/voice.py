from typing import cast

import discord
from discord import app_commands
from discord.ext import commands

from config import (
    VERGONHA_CHANNEL,
    FREESTYLE_CHANNEL,
    MESADEBAR_CHANNEL,
    LOG_CHANNEL,
    BARMAN_ROLE,
    FREESTYLE_ROLE,
)
from utils import voice_move
from views import Confirm

from .common import CommonCog


class VoiceCogGroup(app_commands.Group):
    ...


class VoiceCog(CommonCog):
    voice = VoiceCogGroup(name="voice", description="Comandos para os canais de voz")

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

        self.bot.tree.add_command(app_commands.ContextMenu(name="> Castigo", callback=self.move_to_castigo))
        self.bot.tree.add_command(app_commands.ContextMenu(name="> Mesa de Bar", callback=self.move_to_mesadebar))
        self.bot.tree.add_command(app_commands.ContextMenu(name="> Freestyle", callback=self.move_to_freestyle))

    async def move_to_castigo(self, interaction: discord.Interaction, user: discord.Member):
        log_channel = cast(discord.TextChannel, self.bot.get_channel(LOG_CHANNEL))

        user_avatar_url = user.avatar.url if user.avatar else user.default_avatar.url

        em = (
            discord.Embed(
                color=discord.Color.red(),
                description=f"O usuário {user.mention} foi movido para o canal de castigo.",
            )
            .set_author(
                name=f"{user.display_name}#{user.discriminator}",
                icon_url=user_avatar_url,
            )
            .add_field(name="ID", value=user.id)
        )

        await voice_move(interaction, user, VERGONHA_CHANNEL)
        await log_channel.send(embed=em)

    async def move_to_mesadebar(self, interaction: discord.Interaction, user: discord.Member):
        await voice_move(interaction, user, MESADEBAR_CHANNEL)

    async def move_to_freestyle(self, interaction: discord.Interaction, user: discord.Member):
        await voice_move(interaction, user, FREESTYLE_CHANNEL)

    @app_commands.command(description="Nuke a call.")
    async def nuke_call(self, interaction: discord.Interaction):
        log_channel = cast(discord.TextChannel, self.bot.get_channel(LOG_CHANNEL))

        view = Confirm()
        guild = cast(discord.Guild, interaction.guild)
        nuke_author = cast(discord.Member, guild.get_member(interaction.user.id))

        if not nuke_author.voice:
            await interaction.response.send_message(
                "Você precisa estar em uma call para usar esse comando.",
                ephemeral=True,
                delete_after=5.0,
            )
            return

        nuke_target = cast(discord.VoiceChannel, nuke_author.voice.channel)

        if nuke_target.id == MESADEBAR_CHANNEL:
            members_ping = BARMAN_ROLE
        elif nuke_target.id == FREESTYLE_CHANNEL:
            members_ping = FREESTYLE_ROLE
        else:
            return

        await interaction.response.send_message(
            content="Tem certeza que deseja NUKAR a call?",
            view=view,
            ephemeral=True,
            delete_after=15.0,
        )

        await view.wait()
        if view.value is None:
            return
        elif view.value:
            await nuke_target.send(content=f"||<@&{members_ping}>|| \n Recebam o excesso de democracia.")
            membernames = []
            for member in nuke_target.members:
                if member == nuke_author:
                    continue
                await member.edit(mute=True)
                membernames.append(member.mention)

            log_channel = cast(discord.TextChannel, self.bot.get_channel(LOG_CHANNEL))
            user_avatar_url = (
                interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url
            )
            em = (
                discord.Embed(
                    color=discord.Color.red(),
                    description=f"O usuário {interaction.user.mention} nukou a call <#{nuke_target.id}>.",
                )
                .set_author(
                    name=f"{interaction.user}",
                    icon_url=user_avatar_url,
                )
                .add_field(name="Membros nukados:", value=", ".join(membernames))
            )

            await log_channel.send(embed=em)

    @app_commands.command(description="Unuke a call.")
    async def unnuke_call(self, interaction: discord.Interaction):
        guild = cast(discord.Guild, interaction.guild)
        nuke_author = cast(discord.Member, guild.get_member(interaction.user.id))

        if not nuke_author.voice:
            return

        nuke_target = cast(discord.VoiceChannel, nuke_author.voice.channel)

        if nuke_target.id == MESADEBAR_CHANNEL:
            members_ping = BARMAN_ROLE
        elif nuke_target.id == FREESTYLE_CHANNEL:
            members_ping = FREESTYLE_ROLE
        else:
            return

        for member in nuke_target.members:
            if member == nuke_author:
                continue
            await member.edit(mute=False)

        await nuke_target.send(content=f"||<@&{members_ping}>|| \n Call desnukeada.")
        await interaction.response.send_message("Call desnukeada.", ephemeral=True, delete_after=5.0)


async def setup(bot):
    await bot.add_cog(VoiceCog(bot))
