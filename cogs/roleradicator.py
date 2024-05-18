from vote import vote, Importance
import discord
from discord.ext import commands
from discord.utils import get

class RoleRemove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='remove_role')
    async def remove_role(self, ctx, user_name: str, role_name: str):
        # user selection
        member = discord.utils.get(ctx.guild.members, name=user_name)
        if member is None:
            await ctx.send("Пользователь не найден.")
            return

        # role selection
        role = get(ctx.guild.roles, name=role_name)
        if role is None:
            await ctx.send("Роль не найдена.")
            return

        # execution (literally)
        choice = await vote(self.bot, ctx, f"Уберём у пользователя {user_name} роль {role_name}?", ["Да", "Нет"], symbols='thumbs', importance=Importance.medium) #returned the standart medium value
        if choice.pop() == 1:
            await ctx.send("Голосование не подтверждено.")
            return

        try:
            # eradication
            await member.remove_roles(role)
            await ctx.send(f"Роль {role_name} успешно удалена у пользователя {member.name}. It's over...")
        except discord.Forbidden:
            await ctx.send("Я генетически непригоден для выполнения этой операции.")
        except Exception as e:
            await ctx.send(f"Ошибка при удалении роли: {e}")

async def setup(bot):
    await bot.add_cog(RoleRemove(bot))
