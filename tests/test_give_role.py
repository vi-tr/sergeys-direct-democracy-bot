import discord
import discord.ext.commands as commands
from discord.ext.commands import Cog, command
import pytest
import pytest_asyncio
import discord.ext.test as dpytest
import os

@pytest_asyncio.fixture
async def bot():
    # Setup
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    b = commands.Bot(command_prefix="/",
                     intents=intents)
    await b._async_setup_hook()  # setup the loop
    await b.load_extension("cogs.role_give")

    dpytest.configure(b)

    yield b

    # Teardown
    await dpytest.empty_queue() # empty the global message queue as test teardown


@pytest.mark.asyncio
async def test_ping(bot):
    await dpytest.message("/test_give_role test_name test_role "+ os.getenv('BOT_TOKEN'))
    assert dpytest.verify().message().contains().content("Роль не найдена")
