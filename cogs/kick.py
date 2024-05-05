import discord
from discord.ext import commands

from vote import vote, Importance


class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='kick_member')
    async def kick_member(self, ctx, member: discord.Member):

        choice = await vote(self.bot, ctx=ctx, title=f"Выгнать ли {member} с сервера?", options=["Да", "Нет"],
                            symbols='thumbs', importance=Importance.medium)
        if choice.pop() == 1:
            await ctx.send("Голосование провалилось")
        else:
            await ctx.send(f"{member} был изгнан")
            await member.kick()


async def setup(bot):
    await bot.add_cog(Kick(bot))
