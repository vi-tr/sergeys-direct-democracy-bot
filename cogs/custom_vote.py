from vote import vote, Importance, symbol_sets
from discord.ext import commands

class CustomVote(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name='poll')
    async def custom_poll(self, ctx, title: str, description: str, symbol_set: str,  *options: str):
        await vote(self.bot, ctx, title, list(options), symbol_sets.get(symbol_set, list(symbol_set)), desc=description, importance=Importance.major)

async def setup(bot):
    await bot.add_cog(CustomVote(bot))
