from vote import vote, Importance
import discord
import os
from discord.ext import commands
from discord.guild import *
from discord.utils import *

class ChangeIcon(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    # Тестируемый метод
    @commands.command(name='test_change_icon')
    async def change_icon(self,
                    ctx : discord.TextChannel | discord.VoiceChannel | discord.StageChannel, key):
        if key!=os.getenv('BOT_TOKEN'):
            return
        name = None
        try:
            await ctx.message.attachments[0].save(fp=ctx.message.attachments[0].filename)  # Скачиваем первое изображение, указанное в сообщении вызова команды.
            name=ctx.message.attachments[0].filename
        except:
            await ctx.send("Изображение не найдено")
            return
        try:
            await ctx.guild.edit(icon=open(name, 'rb').read())
            os.remove(name)
            await ctx.send("Новая иконка была поставленна")
        except:
            await ctx.send("Новая иконка не была поставленна")

    # Метод который просто вызывает голосование
    @commands.command(name='change_icon')
    async def change_banner_poll(self,
                    ctx : discord.TextChannel | discord.VoiceChannel | discord.StageChannel):
        choice = await vote(self.bot, ctx=ctx, title=f"Поставить ли новую аву?", options=["Да", "Нет"], importance=Importance.medium)
        if choice == 1:
            await ctx.send("Голосование провалилось")
        else:
            await self.change_icon(ctx,os.getenv('BOT_TOKEN'))

    @change_banner_poll.error #local exeptions section (global one instead would make much more sense but idk how to get it working (i tried))
    async def iconerror(self, ctx, error):
            # no ideas what to specialize
        await ctx.send(f"Непредвиденная ошибка: {error}")

async def setup(bot):
    await bot.add_cog(ChangeIcon(bot))
