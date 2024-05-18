import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from discord.ext import commands
from cogs.roleradicator import RoleRemove
from main import INTENTS

@pytest.mark.asyncio
async def test_change_server_name():
   with patch('vote.vote', new=AsyncMock()) as mock_func, patch('discord.Client.wait_for', new_callable=AsyncMock) as mock_wait:
        mock_func.return_value = set([0])
        mock_reaction = MagicMock()
        mock_user = MagicMock()
        mock_reaction.emoji = "👎"
        mock_wait.return_value = (mock_reaction, mock_user)

        bot = commands.Bot(command_prefix="/", intents=INTENTS)
        test_cog = RoleRemove(bot)
        ctx = AsyncMock()
        ctx.guild.members = AsyncMock()
        ctx.guild.edit = AsyncMock()
        ctx.send = AsyncMock()

        user_name = "TestUsername"
        role_name = "TestRole"

        await RoleRemove.remove_role(test_cog,  ctx, user_name, role_name)

        ctx.send.assert_called_with(f"Голосование не подтверждено.")
