import sys
sys.path.insert(0, '.')
from main import INTENTS
from cogs.example import SimpleCog
from discord.ext import commands
import pytest
import pytest_asyncio
import discord.ext.test as dt

@pytest_asyncio.fixture
async def bot():
    # Setup
    b = commands.Bot(command_prefix="/", intents=INTENTS)
    await b._async_setup_hook()  # setup the loop
    await b.add_cog(SimpleCog(b))
    dt.configure(b, members=1)
    yield b
    # Teardown
    await dt.empty_queue() # empty the global message queue as test teardown


@pytest.mark.asyncio
async def test_money(bot):
    await dt.message("/lend_money")
    assert dt.verify().message().content("Неа")
