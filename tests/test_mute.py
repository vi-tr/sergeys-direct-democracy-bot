import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from discord.ext import commands
from cogs.mute import Mute
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
        test_cog = Mute(bot)
        ctx = AsyncMock()
        member = AsyncMock()
        member.edit = AsyncMock()  
        member.mention = "@TestUser"

        await Mute.mute(test_cog, ctx, member)

        member.edit.assert_called_once_with(mute=True)
        ctx.send.assert_called_with(f"Пользователь {member.mention} был замучен.")

@pytest.mark.asyncio
async def test_unmute():
    with patch('vote.vote', new=AsyncMock()) as mock_func, patch('discord.Client.wait_for', new_callable=AsyncMock) as mock_wait:
        mock_func.return_value = set([0])
        mock_reaction = MagicMock()
        mock_user = MagicMock()
        mock_reaction.emoji = "👍"  
        mock_wait.return_value = (mock_reaction, mock_user)

        bot = commands.Bot(command_prefix="/", intents=INTENTS)
        test_cog = Mute(bot)
        ctx = AsyncMock()
        member = AsyncMock()
        member.edit = AsyncMock() 
        member.mention = "@TestUser"

        await Mute.unmute(test_cog, ctx, member)

        member.edit.assert_called_once_with(mute=False)
        ctx.send.assert_called_with(f"Пользователь {member.mention} был размучен.")
