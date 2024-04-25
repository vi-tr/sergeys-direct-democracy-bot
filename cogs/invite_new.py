import discord
from discord.ext import commands

from vote import vote, Importance

class Invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='invite')
    async def invite(self, ctx):
        guild = ctx.guild
        invite = await guild.text_channels[0].create_invite(max_age=0, max_uses=0, temporary=False)

        choice = await vote(self.bot, ctx=ctx, title=f"Пригласить ли нового     пользователя?", options=["Да", "Нет"],
                        symbols='letters', importance=Importance.medium)
        if choice.pop() == 1:
            await ctx.send("Голосование провалилось")
        else:
            await ctx.send("Пользователь скоро будет приглашён")
            await ctx.author.send(f"https://discord.gg/{invite.code}")


async def setup(bot):
    await bot.add_cog(Invite(bot))