import discord
from discord.ext import commands

from vote import vote, Importance


class Textermination(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command("textermination")
    async def delete_text_channel(self, ctx, category: commands.CategoryChannelConverter, channel_name: str):
        guild = ctx.guild
        category_name = category.name  # Получаем имя категории

        channel = discord.utils.get(category.text_channels, name=channel_name)

        if channel is None:
            await ctx.send(f"Текстовый канал '{channel_name}' не найден в категории '{category_name}'.")
            return

        choice = await vote(self.bot, ctx, f"Сносим текстовый канал {channel_name} из категории {category_name}?",
                            ["Да", "Нет"], symbols='thumbs', importance=Importance.minor)
        if choice.pop() == 1:
            await ctx.send("Голосование провалилось")
            return
        else:
            await channel.delete()
            await ctx.send(f"Текстовый канал '{channel_name}' успешно удален из категории '{category_name}'!")


async def setup(bot):
    await bot.add_cog(Textermination(bot))
