import discord
from discord.ext import commands
from vote import vote, Importance

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='create_voice_channel')
    async def create_voice_channel(self, ctx, category_name: str, channel_name: str):
        """
        Создает голосовой канал с заданным именем в заданной категории.
        Пример использования: /create_voice_channel MyCategory MyVoiceChannel
        """
        guild = ctx.guild
        category = discord.utils.get(guild.categories, name=category_name)

        choice = await vote(self.bot, ctx, f"Создать ли голосовой канал {channel_name} в категории {category_name}", ["Да", "Нет"], importance=Importance.medium)
        if choice==1:
            await ctx.send("Голосование провалилось")
            return
        else:
            if category is None:
                category = await guild.create_category(category_name)
                await ctx.send(f"Категория '{category_name}' создана.")

            await guild.create_voice_channel(channel_name, category=category)
            await ctx.send(f"Голосовой канал '{channel_name}' успешно создан в категории '{category_name}'!")

    @create_voice_channel.error #local exceptions section (global one instead would make much more sense but idk how to get it working (i tried))
    async def vcerror(self, ctx, error):
        await ctx.send(f"Непредвиденная ошибка: {error}")


async def setup(bot):
    await bot.add_cog(Voice(bot))
