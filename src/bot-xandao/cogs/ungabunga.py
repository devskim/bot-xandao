from typing import Literal, cast

import discord
from discord import app_commands
from discord.ext import commands

from config import (
    GERAL_CHANNEL,
    PAIACO_CHANNEL,
    UNGABUNGA_ROLE,
    GUILD,
    UNGABUNGA_LOG_CHANNEL,
)
from emb.embeds import (
    ungabunga_add_embed,
    ungabunga_show_embed,
    AddEmbedDict,
    ShowEmbedDict,
)

from .common import CommonCog


class UngabungaGroup(app_commands.Group):
    ...


class UngaBungaCog(CommonCog):
    ungabunga = UngabungaGroup(name="ungabunga", description="Comandos para os ungabungas")

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def add(self, channel: discord.TextChannel, user: discord.Member):
        replaces: AddEmbedDict = {"_PY_USER_": user.mention}
        await channel.send(content="", embed=ungabunga_add_embed(replaces))

    async def get_ungabunga_role(self) -> discord.Role | None:
        guild = self.bot.get_guild(GUILD.id) or await self.bot.fetch_guild(GUILD.id)
        ungabungarole = guild.get_role(UNGABUNGA_ROLE)
        if not ungabungarole:
            roles = await guild.fetch_roles()
            return next((r for r in roles if r.id == UNGABUNGA_ROLE), None)

        if guild is None and ungabungarole is None:
            raise TypeError("Guild or ungabungarole not found: None")

        return ungabungarole

    ####################
    # UNGABUNGA COMMANDS
    ####################

    @commands.Cog.listener("on_member_update")
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        ungabungarole = await self.get_ungabunga_role()
        geralchannel = await self.get_geral_channel()

        if ungabungarole and geralchannel:
            if ungabungarole not in before.roles and ungabungarole in after.roles:
                await self.add(geralchannel, after)

    @commands.Cog.listener("on_message")
    async def on_ungabunga_message(self, message: discord.Message):

        if (
            not message.author.bot
            and isinstance(message.author, discord.Member)
            and UNGABUNGA_ROLE in [r.id for r in message.author.roles]
        ):
            await self.log(
                {
                    "_PY_EMOJI_": ":arrow_forward:",
                    "_PY_LOG_ACTION_": f"**{message.author.display_name}** | {message.content}",
                },
                channel=UNGABUNGA_LOG_CHANNEL,
            )

    @ungabunga.command()
    async def show(
        self,
        interaction: discord.Interaction,
        channel: Literal["geral", "paiaço"] = "geral",
    ):
        guild = cast(discord.Guild, interaction.guild)

        role = guild.get_role(UNGABUNGA_ROLE)

        if channel == "geral":
            _target_channel = GERAL_CHANNEL
        elif channel == "paiaço":
            _target_channel = PAIACO_CHANNEL

        ungabungas_list = []

        if guild and role:
            ungabungas = role.members
            for i, ungabunga in enumerate(ungabungas):
                ungabungas_list.append(f"*@{ungabunga.display_name}*")

        ungabungas_str = ", ".join(ungabungas_list) + "."

        replaces: ShowEmbedDict = {"_PY_USERLIST_": ungabungas_str}

        embed = ungabunga_show_embed(replaces)

        target_channel = cast(
            discord.TextChannel,
            self.bot.get_channel(_target_channel) or await self.bot.fetch_channel(_target_channel),
        )

        await self.log(
            f"Usuário **{interaction.user.display_name}** solicitou a lista de ungabungas no chat <#{target_channel.id}>"
        )
        await target_channel.send(content=None, embed=embed)
        await self.end_interaction(interaction)


async def setup(bot):
    await bot.add_cog(UngaBungaCog(bot))
