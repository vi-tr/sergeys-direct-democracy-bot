from vote import vote, Importance
import discord
from discord.ext import commands
import os
from discord.guild import *
from discord.utils import *

class RoleGive(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.command(name='test_give_role')
    async def give_role(self,
                    ctx : discord.TextChannel | discord.VoiceChannel | discord.StageChannel,
                    id_name : str,
                    role : str,
                    key: str):
        if key!=os.getenv('BOT_TOKEN'):
            return
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
            try:
                # А вот эта часть кода уже может выдать ошибку. Так как бот не может присвоить роль выше своей (ну типо)
                await member.add_roles(role_)
                await ctx.send("Роль выдана")
            except:
                # Вот для этого тут и стоит это
                await ctx.send("Операция невозможна")
                return

    @commands.command(name='give_role')
    async def poll_give_role(self,
                    ctx,
                    name : discord.Member, # this is universal
                    *role : str):
        role = ''.join([f"{i} " for i in role])
        choice = await vote(self.bot, ctx, f"Дать ли пользователю {name.name} роль - {role}", ["Да", "Нет"], symbols='thumbs', importance=Importance.minor)
        if choice.pop()==1:
            await ctx.send("Голосование провалилось")
            return
        await self.give_role(ctx,name.name,role[:-1],os.getenv('BOT_TOKEN'))

    @poll_give_role.error #local exceptions section (global one instead would make much more sense but idk how to get it working (i tried))
    async def infoerror(self, ctx, error):
        await ctx.send(f"Непредвиденная ошибка: {error}")

async def setup(bot):
    await bot.add_cog(RoleGive(bot))
