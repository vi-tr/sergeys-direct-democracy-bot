import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from discord.ext import commands
from cogs.change_server_name import ServerManagement
from main import INTENTS

@pytest.mark.asyncio
async def test_change_server_name():
   with patch('vote.vote', new=AsyncMock()) as mock_func, patch('discord.Client.wait_for', new_callable=AsyncMock) as mock_wait:
        mock_func.return_value = set([0])
        mock_reaction = MagicMock()
        mock_user = MagicMock()
        mock_reaction.emoji = "👍"
        mock_wait.return_value = (mock_reaction, mock_user)

        bot = commands.Bot(command_prefix="/", intents=INTENTS)
        test_cog = ServerManagement(bot)
        ctx = MagicMock()
        ctx.guild.edit = AsyncMock()
        ctx.send = AsyncMock()

        new_name = "TestServer"

        await ServerManagement.change_server_name(test_cog, ctx, new_name=new_name)

        ctx.guild.edit.assert_called_once_with(name=new_name)
        ctx.send.assert_called_with(f'Имя сервера было успешно изменено на {new_name}')
