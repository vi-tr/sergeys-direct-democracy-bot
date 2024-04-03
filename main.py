import logging
import discord
from discord.ext import commands
from typing import Final
import os
import asyncio

# Токен передаем через .env файл, если хотите его узнать, пишите мне, Антону или Вите
TOKEN: Final[str|None] = os.getenv('BOT_TOKEN')
assert TOKEN is not None, "Токен не найден, проверьте что переменная окружения $BOT_TOKEN содержит токен"

# это полное разрешение на все действия, иначе реализовать это походу не получится
bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

# здесь не нужно ничего трогать
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    discord.utils.setup_logging(level=logging.INFO)
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == "__main__": asyncio.run(main())

# PS Писать свои функции, нужно в отдельных файлах в папке cogs 
