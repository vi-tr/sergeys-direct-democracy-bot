import discord
from discord.ext import commands
from vote import vote, Importance

class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='mute')
    async def mute(self, ctx, member: discord.Member):
        choice = await vote(self.bot, ctx, f"Замутить ли пользователя {member.name}", ["Да", "Нет"], symbols='thumbs', importance=Importance.minor)
        if choice.pop()==1:
            await ctx.send("Голосование провалилось")
            return
        await member.edit(mute=True)
        await ctx.send(f"Пользователь {member.mention} был замучен.")

    @commands.command(name='unmute')
    async def unmute(self, ctx, member: discord.Member):
        choice = await vote(self.bot, ctx, f"Размутить ли пользователя {member.name}", ["Да", "Нет"], symbols='thumbs', importance=Importance.medium)
        if choice.pop()==1:
            await ctx.send("Голосование провалилось")
            return
        await member.edit(mute=False)
        await ctx.send(f"Пользователь {member.mention} был размучен.")


async def setup(bot):
    await bot.add_cog(Mute(bot))

    '''
        if not muted_role:
            try:
                muted_role = await ctx.guild.create_role(name="Muted")

                for channel in ctx.guild.channels:
                    await channel.set_permissions(muted_role, speak=False, send_messages=True)
            except discord.Forbidden:
                return await ctx.send("У меня нет разрешения на создание роли.")
        '''

    """
import discord
from discord.ext import commands

class Unmute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='unmute')
    async def unmute(self, ctx, member: discord.Member):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            return await ctx.send("Роль 'Muted' не найдена. Пользователь не может быть размучен.")
        await member.remove_roles(muted_role)
        await ctx.send(f"{member.mention} был размучен.")

async def setup(bot):
    await bot.add_cog(Unmute(bot))
"""
