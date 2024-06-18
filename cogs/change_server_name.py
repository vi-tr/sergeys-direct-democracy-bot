import discord
from discord.ext import commands
from vote import vote, Importance

class ServerManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='change_server_name')
    async def change_server_name(self, ctx, *, new_name: str):
        choice = await vote(self.bot, ctx, f"Сменить имя сервера на {new_name}", ["Да", "Нет"], importance=Importance.minor)
        if choice.pop()==1:
            await ctx.send("Голосование провалилось")
            return

        else:
            try:
                await ctx.guild.edit(name=new_name)
                await ctx.send(f'Имя сервера было успешно изменено на {new_name}')
            except Exception as e:
                await ctx.send(f'Произошла ошибка при изменении имени сервера: {e}')

async def setup(bot):
    await bot.add_cog(ServerManagement(bot))
