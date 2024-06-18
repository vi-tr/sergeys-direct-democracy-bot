import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from discord.ext import commands
import discord
from main import INTENTS
from cogs.add_role import AddRole, CustomRole


@pytest.mark.asyncio
async def test_addrole():
    with patch('vote.vote', new=AsyncMock()) as mock_func, patch('discord.Client.wait_for', new_callable=AsyncMock) as mock_wait:
        mock_func.retun_value = set([0])
        mock_reaction = MagicMock()
        mock_user = MagicMock()
        mock_reaction.emoji = "👍"
        mock_wait.return_value = (mock_reaction, mock_user)

        bot = commands.Bot(command_prefix='/', intents=INTENTS)

        test_cog = AddRole(bot)

        test_role_perm = "member"
        test_role_obj = CustomRole()
        test_role_type = test_role_obj.get_role_permissions_factory(test_role_perm)

        r, g, b = 0, 0, 0
        test_role_name = "Test Role Name"

        ctx = AsyncMock()
        ctx.reply = AsyncMock()
        ctx.guild.create_role = AsyncMock()

        await AddRole.create_role(test_cog, ctx, test_role_perm, r, g, b, test_role_name)

        ctx.guild.create_role.assert_called_once_with(
        name=test_role_name,
        color=discord.Colour.from_rgb(int(r), int(g), int(b)),
        permissions=test_role_type
        )
        ctx.reply.assert_called_with("Роль успешно создана!")
