import discord
import asyncio
import time
from datetime import datetime
from typing import List, Set, Final, Tuple, Dict, Callable
from logging import getLogger
from enum import Enum

from math import ceil
from random import choice
from itertools import groupby
from operator import itemgetter, attrgetter

_logger = getLogger(__name__)
_tie_strategy_type = Callable[[Set[int], str, List[str]], int]

global_exclude: List[discord.Member] = []

symbol_sets: Final[Dict[str,List[str]]] = {
    'thumbs': ["👍", "👎"],
    'thumbs3': ["👍", "✊", "👎"],
    'letters': ["🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬", "🇭", "🇮", "🇯", "🇰", "🇱", "🇲", "🇳", "🇴", "🇵", "🇶", "🇷", "🇸", "🇹", "🇺", "🇻", "🇼", "🇽", "🇾"],
    'numbers': ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"],
}

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

def bar_gen(percentage: float, size: int):
    chars: Final[str] = ' ▁▂▃▄▅▆▇█'
    pos = percentage*size
    return '█'*int(pos) + ('' if int(pos)==pos else chars[int(pos%1.0*len(chars))]) + ' '*(size-ceil(pos))

def tie_breaker_random(contest: Set[int], title: str, options: List[str]) -> int:
    return choice(list(contest))

async def vote(client: discord.Client,
        ctx: discord.TextChannel | discord.VoiceChannel | discord.StageChannel,
        title: str, options: List[str],
        symbols: List[str]=symbol_sets['thumbs'], exclude=[],
        timeout: float|None=None, count: float|None=None,
        desc: str|None=None, importance: Importance=Importance.medium,
        tie_strategy: _tie_strategy_type = tie_breaker_random) -> int:
    result = await _unwrapped_vote(client, ctx, title, options, symbols, exclude, timeout, count, desc, importance, tie_strategy)
    assert type(result) is int
    return result

async def vote_multiple_result(client: discord.Client,
        ctx: discord.TextChannel | discord.VoiceChannel | discord.StageChannel,
        title: str, options: List[str],
        symbols: List[str]=symbol_sets['thumbs'], exclude=[],
        timeout: float|None=None, count: float|None=None,
        desc: str|None=None, importance: Importance=Importance.medium) -> Set[int]:
    result = await _unwrapped_vote(client, ctx, title, options, symbols, exclude, timeout, count, desc, importance, None)
    assert type(result) is Set[int]
    return result

async def _unwrapped_vote(client: discord.Client,
        # Equivalent to the overlap of abc.Messageable and abc.GuildChannel.
        # Don't know the proper way to do this in python yet.
        ctx: discord.TextChannel | discord.VoiceChannel | discord.StageChannel,
        title: str, options: List[str],
        symbols: List[str]=symbol_sets['thumbs'], exclude=[],
        timeout: float|None=None, count: float|None=None,
        desc: str|None=None, importance: Importance=Importance.medium,
        tie_strategy: _tie_strategy_type | None = tie_breaker_random) -> int | Set[int]:

    endtime = time.time() + (importance.timeout() if timeout is None else timeout)
    count = max(1, int(len(ctx.guild.members) * (importance.count() if count is None else count))) # Floor, not round
    exclude_ids = set(map(attrgetter('id'), exclude + global_exclude))

    embed = discord.Embed(title=title,
        description=f"{desc or ''}\nГолосование будет окончено автоматически в {datetime.fromtimestamp(endtime).strftime('%Y-%m-%d %H:%M:%S')}, либо когда проголосуют {count} человек(а).",
        colour=0xed333b, timestamp=datetime.now()
    )
    embed.set_author(name="Голосование")
    assert len(options) <= len(symbols), 'Количество опций голосование превышает количество доступных символов'

    for i, f in enumerate(options): embed.add_field(name=f, value=symbols[i]+" (0)", inline=False)
    msg = await ctx.send(embed=embed)
    for i in range(len(options)): await msg.add_reaction(symbols[i])
    _logger.info(f"Vote {msg.id} started")
    result: Set[int] = set()
    try:
        votes: Dict[int,int] = {}
        vote_amounts: List[Tuple[int,int]] = []
        while len(votes) < count:
            add, remove = asyncio.create_task(client.wait_for('reaction_add')), asyncio.create_task(client.wait_for('reaction_remove'))
            first = (await asyncio.wait([add, remove], return_when=asyncio.FIRST_COMPLETED, timeout=endtime-time.time()))[0].pop()
            try: idx = symbols.index(str(first.result()[0].emoji))
            except ValueError: continue
            if first is add:
                remove.cancel()
                user=add.result()[1].id
                if user not in exclude_ids: votes[user]=idx
            else:
                add.cancel()
                user=remove.result()[1].id
                if user not in exclude_ids:
                    try: del votes[user]
                    except KeyError: _logger.warning(f"Somehow a non-existent vote on {msg.id} was removed.")

            vote_amounts = [(k,sum(1 for _ in v)) for k,v in groupby(sorted(votes.values()))]
            dvotes = dict(vote_amounts)
            for i in range(len(options)):
                embed.set_field_at(i, name=embed.fields[i].name, value=f"{symbols[i]} {bar_gen(dvotes.get(i,0)/max(1,len(votes)),20)} ({dvotes.get(i,0)})", inline=False)
            await msg.edit(embed=embed)
        max_vl = max(vote_amounts,key=itemgetter(1))
        result = set(m[0] for m in vote_amounts if m[1]==max_vl[1])
        _logger.info(f"Vote {msg.id} finished successfully.")
    except asyncio.TimeoutError: _logger.info(f"Vote {msg.id} timed out")
    if tie_strategy is None:
        type_check_set: Set[int] = result
        return type_check_set
    else:
        i: int = tie_strategy(result, title, options)
        embed.set_field_at(i, name='*'+(embed.fields[i].name or '')+'*', value=embed.fields[i].value, inline=False)
        await msg.edit(embed=embed)
        return i
