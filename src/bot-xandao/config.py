# fmt: off
import os
import discord

GUILD = discord.Object(os.environ["GUILD"])
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]


BALCAO_CHANNEL = int(os.environ["BALCAO_CHANNEL"])
UNGABUNGA_ROLE = int(os.environ["UNGABUNGA_ROLE"])
COMMANDS_CHANNEL = int(os.environ["COMMANDS_CHANNEL"])
GERAL_CHANNEL = int(os.environ["GERAL_CHANNEL"])
PAIACO_CHANNEL = int(os.environ["PAIACO_CHANNEL"])
VERGONHA_CHANNEL = int(os.environ["VERGONHA_CHANNEL"])
MESADEBAR_CHANNEL = int(os.environ["MESADEBAR_CHANNEL"])
BARMAN_ROLE = int(os.environ["BARMAN_ROLE"])
FREESTYLE_CHANNEL = int(os.environ["FREESTYLE_CHANNEL"])
FREESTYLE_ROLE = int(os.environ["FREESTYLE_ROLE"])
LOG_CHANNEL = int(os.environ["LOG_CHANNEL"])
UNGABUNGA_LOG_CHANNEL = int(os.environ["UNGABUNGA_LOG_CHANNEL"])
