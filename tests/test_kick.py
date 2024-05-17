import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from discord.ext import commands
from cogs.kick import Kick
from main import INTENTS

@pytest.mark.asyncio
async def test_mute():
   with patch('vote.vote', new=AsyncMock()) as mock_func, patch('discord.Client.wait_for', new_callable=AsyncMock) as mock_wait:
        mock_func.return_value = set([0])
        mock_reaction = MagicMock()
        mock_user = MagicMock()
        mock_reaction.emoji = "👍"
        mock_wait.return_value = (mock_reaction, mock_user)

        bot = commands.Bot(command_prefix="/", intents=INTENTS)
        test_cog = Kick(bot)
        ctx = AsyncMock()
        member = AsyncMock()
        member.edit = AsyncMock()
        member.mention = "@TestUser"
        member1 = AsyncMock()
        member1.edit = AsyncMock()
        member1.mention = "@TestUser1"

        await Kick.kick_member(test_cog, ctx, member1)

        ctx.send.assert_called_with("Пользователь был изгнан")
