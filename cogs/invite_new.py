import discord
from discord.ext import commands

from vote import vote, Importance

class Invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='invite')
    async def invite(self, ctx):
        guild = ctx.guild

        choice = await vote(self.bot, ctx=ctx, title=f"Пригласить ли нового пользователя?", options=["Да", "Нет"], importance=Importance.minor)
        if choice == 1:
            await ctx.send("Голосование провалилось")
        else:
            invite = await guild.text_channels[0].create_invite(max_age=0, max_uses=0, temporary=False)
            await ctx.send("Пользователь скоро будет приглашён")
            await ctx.author.send(f"https://discord.gg/{invite.code}")

    @invite.error
    async def inviteerror(self, ctx, error):
        await ctx.send(f"Непредвиденная ошибка: {error}")


async def setup(bot):
    await bot.add_cog(Invite(bot))
