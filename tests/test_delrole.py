import sys
import os
import pytest_asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from discord.ext import commands
import discord
from main import INTENTS
from cogs.del_role import DeleteRole

@pytest.mark.asyncio
async def test_addrole():
    with patch('vote.vote', new=AsyncMock()) as mock_func, patch('discord.Client.wait_for', new_callable=AsyncMock) as mock_wait:
        mock_func.return_value = set([0])
        mock_reaction = MagicMock()
        mock_user = MagicMock()
        mock_reaction.emoji = "👎"
        mock_wait.return_value = (mock_reaction, mock_user)

        bot = commands.Bot(command_prefix='/', intents=INTENTS)

        test_cog = DeleteRole(bot)
        test_role_name = "Test Roles"

        ctx = AsyncMock()
        ctx.reply = AsyncMock()
        ctx.discord.utils.get.delete = AsyncMock()

        await DeleteRole.del_role(test_cog, ctx, test_role_name)

        ctx.reply.assert_called_with("Голосование провалилось.")
