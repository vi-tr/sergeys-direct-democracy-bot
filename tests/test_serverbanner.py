import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from unittest.mock import AsyncMock, MagicMock, mock_open, patch
from discord.ext import commands
from cogs.change_banner import ChangeIcon  
from main import INTENTS

@pytest.mark.asyncio
async def test_change_banner():
    with patch('vote.vote', new=AsyncMock()) as mock_func, patch('discord.Client.wait_for', new_callable=AsyncMock) as mock_wait, patch('builtins.open', mock_open(read_data=b"test")) as mock_file, patch('os.remove') as mock_remove:
        mock_func.return_value = set([0])
        mock_reaction = MagicMock()
        mock_user = MagicMock()
        mock_reaction.emoji = "👍"  
        mock_wait.return_value = (mock_reaction, mock_user)

        bot = commands.Bot(command_prefix="/", intents=INTENTS)
        test_cog = ChangeIcon(bot)
        ctx = MagicMock()
        ctx.message.attachments = [MagicMock()]
        ctx.message.attachments[0].filename = "test.png"
        ctx.message.attachments[0].save = AsyncMock()
        ctx.guild.edit = AsyncMock()
        ctx.send = AsyncMock()

        await ChangeIcon.change_banner(test_cog, ctx)

        ctx.message.attachments[0].save.assert_called_once()
        ctx.guild.edit.assert_called_once()
        ctx.send.assert_called_with("Новая ава поставлена")
