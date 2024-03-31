import logging
import discord
from discord.ext import commands
from typing import Final
import os
import asyncio

# Токен передаем через .env файл, если хотите его узнать, пишите мне, Антону или Вите
TOKEN: Final[str|None] = os.getenv('BOT_TOKEN')
assert TOKEN is not None, "Токен не найден, проверьте что переменная окружения $BOT_TOKEN содержит токен"

#инициализация бота должна находиться в глобальной области видимости,
#так как из main обьект класса Client никто не увидит
INTENTS: Final[discord.Intents] = discord.Intents(
    message_content=True, # TODO: App/hybrid commands since apparently no one else can figure them out
    messages=True,
    members=True,
    guild_reactions=True,
    typing=False,
    presences=False,
)
bot = commands.Bot(command_prefix="/", intents=INTENTS)

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
