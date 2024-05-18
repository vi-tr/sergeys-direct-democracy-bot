import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from discord.ext import commands
from cogs.new_voice import Voice
from cogs.voicexecution import Voicexecution
from main import INTENTS

@pytest.mark.asyncio
async def test_create_voice():
   with patch('vote.vote', new=AsyncMock()) as mock_func, patch('discord.Client.wait_for', new_callable=AsyncMock) as mock_wait:
        mock_func.return_value = set([0])
        mock_reaction = MagicMock()
        mock_user = MagicMock()
        mock_reaction.emoji = "👍"
        mock_wait.return_value = (mock_reaction, mock_user)

        bot = commands.Bot(command_prefix="/", intents=INTENTS)
        test_cog = Voice(bot)
        ctx = AsyncMock()
        ctx.guild.members = AsyncMock()
        ctx.guild.categories = AsyncMock()
        ctx.guild.edit = AsyncMock()
        ctx.send = AsyncMock()

        category_name = "TestName"
        channel_name = "TestChanel"

        await Voice.create_voice_channel(test_cog,  ctx, category_name, channel_name)

        ctx.send.assert_called_with( f"Голосовой канал '{channel_name}' успешно создан в категории '{category_name}'!")

@pytest.mark.asyncio
async def test_delete_voice():
   with patch('vote.vote', new=AsyncMock()) as mock_func, patch('discord.Client.wait_for', new_callable=AsyncMock) as mock_wait:
        mock_func.return_value = set([0])
        mock_reaction = MagicMock()
        mock_user = MagicMock()
        mock_reaction.emoji = "👎"
        mock_wait.return_value = (mock_reaction, mock_user)

        bot = commands.Bot(command_prefix="/", intents=INTENTS)
        test_cog = Voicexecution(bot)
        ctx = AsyncMock()
        ctx.guild.members = AsyncMock()
        ctx.guild.categories = AsyncMock()
        ctx.guild.edit = AsyncMock()
        ctx.send = AsyncMock()

        category_name = AsyncMock()
        category_name.name = "TestCategory"
        category_name.voice_channels = AsyncMock()
        channel_name = "TestChanel"

        await Voicexecution.delete_voicechannel(test_cog,  ctx, category_name, channel_name)

        ctx.send.assert_called_with( "Голосование провалилось")
