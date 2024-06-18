import discord
from discord import Permissions
from datetime import datetime, timedelta
from discord.ext import commands, tasks
import vote
import asyncio

class Jail(commands.Cog):
    jailed_users = []
    jail_voices = []
    jail_texts = []
    jail_time = []
    jail_time_bound = []
    def __init__(self, bot):
        self.bot = bot
        self.unjail_task = self.unjail_users.start()

    async def jail(self, ctx, member: discord.Member, time: int):
        """Поместить пользователя в тюрьму на указанное количество минут."""
        if member == None:
            await ctx.send("Юзер не найден")
            return
        voice = discord.utils.get(ctx.guild.voice_channels, name="jail_voice")
        if voice == None:
            await ctx.guild.create_voice_channel("jail_voice")
            voice = discord.utils.get(ctx.guild.voice_channels, name="jail_voice")
        try:
            await member.move_to(voice)
        except:
            pass
        text = discord.utils.get(ctx.guild.text_channels, name="jail_text")
        if text == None:
            await ctx.guild.create_text_channel("jail_text")
            text = discord.utils.get(ctx.guild.text_channels, name="jail_text")
        self.jailed_users.append(member)
        self.jail_voices.append(voice)
        self.jail_texts.append(text)
        self.jail_time.append(datetime.now())
        self.jail_time_bound.append(time)
        await asyncio.sleep(60*time)

    @commands.command("go_to_jail")
    async def poll_jail(self,ctx,member: discord.Member,time:str, *reason):
        reason = ''.join([f" {i}" for i in reason])

        try:
            time=int(float(time))
            if time<=0:
                await ctx.send("Задано нереальное время")
                return
            if time>10:
                await ctx.send("Максимальное время тюремного заключения - 10 минут")
                return
            if discord.utils.get(ctx.guild.members, name=member) in self.jailed_users:
                await ctx.send("Пользователь итак в тюрьме")
                return
        except:
            await ctx.send("Задано нереальное время")
            return
        choice = await vote.vote(self.bot, ctx, f"Посадить ли пользователя {member} на {time} минут за{reason}", ["Да", "Нет"], importance=vote.Importance.minor)
        if choice.pop()==0:
            await ctx.send(f"{member} отправился в тюрьму на {time} минут, за{reason}")
            await self.jail(ctx,member,int(time))
        else: await ctx.send(f"{member} остался на свободе")

    @tasks.loop(seconds=60)
    async def unjail_users(self):
        """Освободить пользователей из тюрьмы по истечении срока."""
        for i in range(len(self.jailed_users)):
            if (datetime.now()-self.jail_time[i])>=timedelta(minutes=self.jail_time_bound[i]):
                self.jailed_users.remove(self.jailed_users[i])
                self.jail_voices.remove(self.jail_voices[i])
                self.jail_texts.remove(self.jail_texts[i])
                self.jail_time.remove(self.jail_time[i])
                self.jail_time_bound.remove(self.jail_time_bound[i])
        vote.global_exclude = self.jailed_users

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Переместить пользователя в голосовой канал тюрьмы, если он покидает его."""
        if member in self.jailed_users:
            if after.channel not in self.jail_voices:
                await member.move_to(self.jail_voices[self.jailed_users.index(member)])

    @commands.Cog.listener()
    async def on_message(self, message):
        """Удалить сообщения, отправленные пользователями тюрьмы вне текстового канала тюрьмы."""
        if message.author in self.jailed_users:
            if message.channel not in self.jail_texts:
                await message.delete()

    @poll_jail.error #local exceptions handler
    async def jailerror(self, ctx, error):
        await ctx.send(f"Непредвиденная ошибка: {error}")


async def setup(bot):
    await bot.add_cog(Jail(bot))
