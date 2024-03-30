# импорты
import discord
from discord import Intents, Client, Message
from discord.ext import commands
from typing import *
import os
import asyncio

from discord import app_commands

# Токен передаем через .env файл, если хотите его узнать, пишите мне, Антону или Вите
TOKEN: Final[str] = os.getenv('BOT_TOKEN')

#инициализация бота должна находиться в глоабльной области видимости,
#так как из main обьект класса Client никто не увидит
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(
    command_prefix="/",
    intents = intents
)

# здесь не нужно ничего трогать
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

# Ещё одна точка входа
async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

# Точка входа
if __name__ == "__main__":
    asyncio.run(main())

# PS Писать свои функции, нужно в отдельных файлах в папке cogs 