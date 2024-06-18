import discord
from discord.ext import commands

from vote import vote, Importance


class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='kick_member')
    async def kick_member(self, ctx, member: discord.Member):

        choice = await vote(self.bot, ctx=ctx, title=f"Выгнать ли {member} с сервера?", options=["Да", "Нет"], importance=Importance.minor)
        if choice.pop() == 1:
            await ctx.send("Голосование провалилось")
        else:
            await ctx.send(f"Пользователь был изгнан")
            await member.kick()

    @kick_member.error #local exceptions section (global one instead would make much more sense but idk how to get it working (i tried))
    async def infoerror(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send("Пользователь не найден.") #(yes I did membernotfound exception for testing)
        else:
            await ctx.send(f"Непредвиденная ошибка: {error}")

async def setup(bot):
    await bot.add_cog(Kick(bot))
