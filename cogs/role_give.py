from vote import vote, Importance
import discord
from discord.ext import commands
from discord.guild import *
from discord.utils import *

class RoleGive(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.command(name='give_role')
    async def give_role(self,
                    ctx : discord.TextChannel | discord.VoiceChannel | discord.StageChannel,
                    id_name : str,
                    role : str):
        # Это часть кода возвращает либо роль, либо ничего, пожтому трай/експект тут не катит
        role_ = discord.utils.get(ctx.guild.roles, name=role)
        if role_ == None:
            await ctx.send("Роль не найдена")
            return
        # Аналогично
        member = discord.utils.get(ctx.guild.members, name=id_name)
        if member == None:
            await ctx.send("Юзер не найден")
            return
        else:
            choice = await vote(self.bot, ctx, f"Дать ли пользователю {id_name} роль - {role}", ["Да", "Нет"], symbols='letters', importance=Importance.medium)
            if choice.pop()==1:
                await ctx.send("Голосование провалилось")
                return
            try:
                # А вот эта часть кода уже может выдать ошибку. Так как бот не может присвоить роль выше своей (ну типо)
                await member.add_roles(role_)
                await ctx.send("Роль выдана")
            except:
                # Вот для этого тут и стоит это
                await ctx.send("Операция невозможна")
                return

async def setup(bot):
    await bot.add_cog(RoleGive(bot))
