import discord
from discord import Intents, Client, Message
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(
    command_prefix="!",
    intents = intents
)