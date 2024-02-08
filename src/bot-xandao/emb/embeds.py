from typing import TypeAlias, TypedDict, cast
import discord
import json
from pathlib import Path
import io
import pytz
import datetime

ChannelMention: TypeAlias = str
UserMention: TypeAlias = str
UserString: TypeAlias = str
UserStrList: TypeAlias = str
DateTime: TypeAlias = str


class AddEmbedDict(TypedDict, total=False):
    _PY_USER_: UserMention
    _PY_DATETIME_: DateTime


class ShowEmbedDict(TypedDict, total=False):
    _PY_USERLIST_: UserStrList
    _PY_DATETIME_: DateTime


class LogDict(TypedDict, total=False):
    _PY_EMOJI_: str
    _PY_LOG_ACTION_: str


EmbedReplaces: TypeAlias = AddEmbedDict | ShowEmbedDict


def get_datetime() -> str:
    tz_sp = pytz.timezone("America/Sao_Paulo")
    created_at = datetime.datetime.now(tz=tz_sp)
    created_at = created_at.strftime("%d/%m/%Y, às %H:%M.")
    return created_at


def open_json(jsonpath):
    data_file_path = Path(__file__).parent / jsonpath

    with io.open(data_file_path, "r", encoding="utf8") as f:
        json_str = f.read()
    return json_str


def base_embed(jsonpath: str, replaces: EmbedReplaces) -> discord.Embed:
    embed_str = open_json(jsonpath)

    replaces.setdefault("_PY_DATETIME_", get_datetime())

    for k, v in replaces.items():
        embed_str = embed_str.replace(k, cast(str, v))

    jsonembed = json.loads(embed_str)
    em = discord.Embed.from_dict(jsonembed)
    return em


def base_log_embed(replaces: LogDict | str) -> discord.Embed:
    logstr = open_json("log.json")

    if isinstance(replaces, dict):
        if "_PY_EMOJI_" not in replaces.keys():
            replaces.setdefault("_PY_EMOJI_", ":white_check_mark:")

        for k, v in replaces.items():
            logstr = logstr.replace(k, cast(str, v))
    else:
        logstr = logstr.replace("_PY_LOG_ACTION_", replaces)

    logdict = json.loads(logstr)
    em = discord.Embed.from_dict(logdict)
    return em

    # return base_embed("log.json", replaces)


def ungabunga_add_embed(replaces: AddEmbedDict):
    return base_embed("ungabunga_add.json", replaces)


def ungabunga_show_embed(replaces: ShowEmbedDict):
    return base_embed("ungabunga_show.json", replaces)


def report_embed(interaction: discord.Interaction, message: discord.Message):
    embed = discord.Embed(title="Mensagem Reportada")
    # Handle report by sending it into a log channel
    if message.content:
        embed.description = message.content
    if message.attachments:
        embed.set_image(url=message.attachments[0].url)

        
    embed.set_author(
        name=message.author.display_name,
        icon_url=message.author.display_avatar.with_format("jpg").url,
    )
    embed.timestamp = message.created_at
    embed.add_field(name="User ID", value=message.author.id)
    embed.add_field(name="Message ID", value=message.id)
    channelid = message.channel.id if isinstance(message.channel, discord.TextChannel) else 0
    embed.set_footer(
        text=f"Reportado por: {interaction.user.display_name}",
        icon_url=interaction.user.display_avatar.with_format("jpg").url,
    )
    embed.add_field(name="Canal", value=f"<#{channelid}>")

    url_view = discord.ui.View()
    url_view.add_item(
        discord.ui.Button(
            label="Mensagem",
            style=discord.ButtonStyle.url,
            url=message.jump_url,
        )
    )
    
    return embed, url_view


# embed_str = embed_str.replace("_PY_DECISAO_", "decisaaaao")
# embed_str = embed_str.replace("_PY_USER_", "usereeeee")
