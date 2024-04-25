from vote import vote, Importance
import discord
import os
from discord.ext import commands
from discord.guild import *
from discord.utils import *

class ChangeIcon(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.command(name='change_icon')
    async def change_banner(self,
                    ctx : discord.TextChannel | discord.VoiceChannel | discord.StageChannel):
        choice = await vote(self.bot, ctx=ctx, title=f"Поставить ли новую аву?", options=["Да", "Нет"],
                        symbols='letters', importance=Importance.medium)
        if choice.pop() == 1:
            await ctx.send("Голосование провалилось")
        else:
            await ctx.message.attachments[0].save(fp=ctx.message.attachments[0].filename)  # Скачиваем первое изображение, указанное в сообщении вызова команды.
            name=ctx.message.attachments[0].filename
            with open(name, 'rb') as image:
                await ctx.guild.edit(icon=image.read())  # При помощи метода read() читаем изображение, и ставим его как баннер на сервере
            os.remove(name)  # Удаляем скачанное изображение
            await ctx.send("Новая ава поставлена")

async def setup(bot):
    await bot.add_cog(ChangeIcon(bot))
