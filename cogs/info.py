import discord
from discord.ext import commands

import discord.ext

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
# mostly debug functions giving raw info to observe
    @commands.command(name='role_info')
    async def role_info(self, ctx, role_input: str): 
        role = discord.utils.get(ctx.guild.roles, id=int(role_input)) if role_input.isdigit() else None

        if role is None:
            role = discord.utils.get(ctx.guild.roles, name=role_input)
        if role is None:
            await ctx.send("Роль не найдена.")
            return
        
        info = (
            f"Название: {role.name}\n"
            f"ID: {role.id}\n"
            f"Цвет: {role.color}\n"
            f"Участники роли: {role.members}\n"
            f"Дата создания: {role.created_at}\n"
            f"Уровень иерархии: {role.position}\n"
            f"Упоминаема ли: {role.mentionable}\n"
            f"Показывается ли отдельно: {role.hoist}\n"
            f"Права роли: {role.permissions}\n"
        )

        await ctx.send(f"Информация о роли {role_input}:\n{info}")

    @commands.command(name='user_info')
    async def user_info(self, ctx, user: discord.Member):        
        info = (
            f"Имя: {user.name}\n"
            f"Дискриминатор: {user.discriminator}\n"
            f"ID: {user.id}\n"
            f"Статус: {user.status}\n"
            f"Создан: {user.created_at}\n"
            f"Бот: {user.bot}\n"
            f"Высшая роль: {user.top_role}\n"
            f"Присоединился: {user.joined_at}\n"
            f"Упоминаемый: {user.mention}"
        )

        await ctx.send(f'Информация о пользователе {user}:\n{info}')

    @user_info.error #local exceptions section (global one instead would make much more sense but idk how to get it working (i tried))
    @role_info.error
    async def infoerror(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send("Пользователь не найден.")
        elif isinstance(error, commands.RoleNotFound):
            await ctx.send("Роль не найдена.")
        else:
            await ctx.send(f"Непредвиденная ошибка: {error}")
            
async def setup(bot):
    await bot.add_cog(Info(bot))