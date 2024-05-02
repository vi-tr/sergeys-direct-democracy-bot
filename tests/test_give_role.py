import pytest
import discord
from discord.ext import commands
import discord.ext.test as dpytest
import os
import asyncio

os.chdir("/home/kemran/sergeys-direct-democracy-bot")

@pytest.mark.asyncio
async def test_give_role():
    INTENTS = discord.Intents(
        message_content=True,
        messages=True,
        members=True,
        guild_reactions=True,
        guilds=True,
        typing=False,
        presences=False,
        voice_states=True,
    )
    bot = commands.Bot(command_prefix="/", intents=INTENTS)
    await bot._async_setup_hook()
    await bot.load_extension("cogs.role_give")
    dpytest.configure(bot)
    await dpytest.message("/test_give_role test_name test_role "+ os.getenv('BOT_TOKEN'))
    assert dpytest.verify().message().contains().content("Роль не найдена")

asyncio.run(test_give_role())
