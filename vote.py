import discord
import asyncio
import time
from datetime import datetime
from typing import List, Set
from logging import getLogger
from enum import Enum

_logger = getLogger(__name__)

class Importance(Enum):
    minor=1; medium=2; major=3
    def timeout(self) -> int:
        match self:
            case Importance.minor: return 3600 # 1 hour
            case Importance.medium: return 259200 # 3 days
            case Importance.major: return 2629800 # 1 month
    def count(self) -> float:
        match self:
            case Importance.minor: return 0.1
            case Importance.medium: return 0.3
            case Importance.major: return 0.6


async def vote(client: discord.Client,
        # Equivalent to the overlap of abc.Messageable and abc.GuildChannel.
        # Don't know the proper way to do this in python yet.
        ctx: discord.TextChannel | discord.VoiceChannel | discord.StageChannel,
        title: str, options: List[str],
        timeout: float|None=None, count: float|None=None,
        desc: str|None=None, importance: Importance=Importance.medium) -> Set[int]:

    endtime = time.time() + (importance.timeout() if timeout is None else timeout)
    count = max(1, int(len(ctx.guild.members) * (importance.count() if count is None else count))) # Floor, not round

    embed = discord.Embed(title=title,
        description=f"{desc or ''}\nГолосование будет окончено автоматически в {datetime.fromtimestamp(endtime).strftime('%Y-%m-%d %H:%M:%S')}, либо когда проголосуют {count} человек(а).",
        colour=0xed333b, timestamp=datetime.now()
    )
    embed.set_author(name="Голосование")
    for f in options: embed.add_field(name=f, value="0", inline=False)
    msg = await ctx.send(embed=embed)
    _logger.info(f"Vote {msg.id} started")
    result = set()
    try:
        votes = 0
        while votes < count:
            add, remove = asyncio.create_task(client.wait_for('reaction_add')), asyncio.create_task(client.wait_for('reaction_remove'))
            first = (await asyncio.wait([add, remove], return_when=asyncio.FIRST_COMPLETED, timeout=endtime-time.time()))[0].pop()
            if first is add:
                remove.cancel()
                votes+=1
            else:
                add.cancel()
                votes-=1
        _logger.info(f"Vote {msg.id} finished successfully")
    except asyncio.TimeoutError: _logger.info(f"Vote {msg.id} timed out")
    return result
