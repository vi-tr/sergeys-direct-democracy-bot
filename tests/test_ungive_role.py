import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from discord.ext import commands
from cogs.roleradicator import RoleRemove
from main import INTENTS

@pytest.mark.asyncio
async def test_remove_role():
    with patch('vote.vote', new=AsyncMock()) as mock_func, patch('discord.Client.wait_for', new_callable=AsyncMock) as mock_wait:
        mock_func.return_value = set([0])
        mock_reaction = MagicMock()
        mock_user = MagicMock()
        mock_reaction.emoji = "👍"
        mock_wait.return_value = (mock_reaction, mock_user)

        # Mocking bot and context
        bot = commands.Bot(command_prefix="/", intents=INTENTS)
        test_cog = RoleRemove(bot)
        ctx = AsyncMock()

        # Mocking member and role
        member = AsyncMock()
        member.mention = "@TestUser"
        ctx.guild.get_member.return_value = member

        role = MagicMock()
        role.name = "testRole"
        ctx.guild.create_role = AsyncMock(return_value=role)
        member.roles = [role]


        # Test the remove_role method
        await RoleRemove.remove_role(test_cog, ctx, "@TestUser", "testRole")

        # Assertions
        member.remove_roles.assert_called_once_with(role)
        ctx.send.assert_called_with("Роль testRole успешно удалена у пользователя @TestUser. It's over...")
