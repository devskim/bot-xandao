import discord
from typing import cast


async def voice_move(
    interaction: discord.Interaction, target_user: discord.Member, target_channel: int
):
    guild = cast(discord.Guild, interaction.guild)
    try:
        _target_channel = cast(discord.VoiceChannel, guild.get_channel(target_channel))
    except:
        raise Exception(f"Channel {target_channel} not found")
    mod_user = cast(discord.Member, guild.get_member(interaction.user.id))

    await mod_user.move_to(_target_channel)
    await target_user.move_to(_target_channel)
    await interaction.response.send_message(
        "Movido com sucesso.", ephemeral=True, delete_after=0.1
    )
